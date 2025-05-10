from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QComboBox, QLineEdit, QTextEdit, QProgressBar, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QIcon
from PyQt5.QtCore import QTimer, QDateTime, Qt

from resources import resource_path
from utils import load_config, save_config
import os
import sys

class MainWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.config = load_config()
        self.current_game = None

        # 顶部控件
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # 添加弹簧推到右边
        self.game_selector = QComboBox()
        self.game_selector.setMaximumWidth(200)
        self.setting_btn = QPushButton("设置 ⚙")
        top_layout.addWidget(self.game_selector)
        top_layout.addWidget(self.setting_btn)

        self.setting_btn.clicked.connect(self.open_settings)
        self.game_selector.currentIndexChanged.connect(self.update_game)

        # 图标和游戏名区域
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(200, 200)
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.game_name_label = QLabel("游戏名称：未选择")
        self.game_name_label.setStyleSheet("""
            font-size: 15px;
            # font-weight: 600;
            font-family: 'SimHei';
            padding-top: 10px;
        """)

        # 使用垂直布局居中图标和文字
        game_info_layout = QVBoxLayout()
        game_info_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        game_info_layout.addWidget(self.game_name_label, alignment=Qt.AlignCenter)

        # 包装在一个 QWidget 里以便加入主布局
        game_info_widget = QWidget()
        game_info_widget.setLayout(game_info_layout)

        # ID 输入
        self.id_label = QLabel("玩家ID:")
        self.id_label.setStyleSheet("font-size: 14px;")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("请输入玩家ID")
        self.boost_btn = QPushButton("申请助力")

        # 名额 + 进度条
        self.quota_label = QLabel("剩余名额: 0")
        self.quota_label.setStyleSheet("font-size: 14px;")
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)  # 不显示百分比文字

        # 日志输出
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(game_info_widget)
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.boost_btn)
        layout.addWidget(self.quota_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.log_box)

        self.setLayout(layout)
        self.populate_games()
        self.boost_btn.clicked.connect(self.start_boost)

    def open_settings(self):
        self.stacked_widget.setCurrentIndex(1) # 显示设置界面
        self.stacked_widget.widget(1).load_config_data()  # 刷新游戏列表

    def populate_games(self):
        old_game_name = self.current_game["game"] if self.current_game else None
        self.game_selector.clear()

        games = self.config.get("games", [])
        for game in games:
            self.game_selector.addItem(game["game"])

        # 还原之前选中的游戏
        if old_game_name:
            index = self.game_selector.findText(old_game_name)
            if index != -1:
                self.game_selector.setCurrentIndex(index)
            else:
                self.game_selector.setCurrentIndex(0)
        elif games:
            self.game_selector.setCurrentIndex(0)

    def update_game(self):
        index = self.game_selector.currentIndex()
        if index < 0:
            return
        self.current_game = self.config["games"][index]
        self.load_image(self.current_game["image"])
        self.game_name_label.setText(self.current_game["game"])  # 新增行
        self.quota_label.setText(f"剩余名额: {self.current_game['quota_number']}")

    def load_image(self, image_name):
        # path = resource_path(image_name)
        path = resource_path(f'images/{image_name}')
        print(path)
        pix = QPixmap(path).scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        rounded = QPixmap(pix.size())
        rounded.fill(Qt.transparent)  # ✅ 关键点：背景透明，保留圆角

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        clip_path = QPainterPath()
        clip_path.addRoundedRect(0, 0, 200, 200, 10, 10)  # ✅ 圆角10
        painter.setClipPath(clip_path)
        painter.drawPixmap(0, 0, pix)
        painter.end()

        self.icon_label.setPixmap(rounded)

    def start_boost(self):
        player_id = self.id_input.text().strip()
        if not player_id or not self.current_game:
            return

        if self.current_game["quota_number"] <= 0:
            now = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            self.log_box.append(f'<span style="color:red">助力名额已满！！！</span>')
            return

        self.progress.setValue(0)
        # self.log_box.append("开始助力中...")
        QTimer.singleShot(200, lambda: self.progress.setValue(25))
        QTimer.singleShot(400, lambda: self.progress.setValue(50))
        QTimer.singleShot(600, lambda: self.progress.setValue(75))
        QTimer.singleShot(800, lambda: self.progress.setValue(100))  # ✅ 先满
        QTimer.singleShot(1000, lambda: self.finish_boost(player_id))  # ✅ 后执行

    def finish_boost(self, player_id):
        prefix = self.config.get("congrats_prefix", "恭喜玩家")
        now = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        for line in self.current_game["text"]:
            self.log_box.append(f'<span style="color:green">{now} {prefix} </span><span style="color:red">{player_id}</span><span style="color:green"> 助力成功:{line}</span>')

        self.current_game["quota_number"] -= 1
        self.quota_label.setText(f"剩余名额: {self.current_game['quota_number']}")
        self.progress.setValue(0)  # ✅ 清空进度条
        save_config(self.config)

