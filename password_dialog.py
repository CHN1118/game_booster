from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon
import sys

class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(320, 180)

        # 创建背景容器
        self.container = QWidget(self)
        self.container.setStyleSheet("""
            QWidget {
                background-color: #282c34;
                border-radius: 15px;
            }
        """)
        self.container.setGeometry(0, 0, 320, 180)

        # 关闭按钮
        self.close_button = QPushButton("✖", self.container)
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                color: #ff6474;
            }
        """)
        self.close_button.clicked.connect(self.reject)
        self.close_button.move(self.width() - 30, 10)  # 调整位置靠右上角

        # 鼠标拖动属性
        self._start_pos = None
        self._is_dragging = False

        # UI 内容
        title = QLabel("🔒 密码验证")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 18px;")
        title.setFont(QFont("Arial", 12, QFont.Bold))

        self.label = QLabel("请输入访问密码:")
        self.label.setStyleSheet("color: white;")

        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1f29;
                color: #ff6474;
                padding: 3px;
                border: 1px solid #555;
                border-radius: 6px;
                font-size: 11px;
            }
        """)

        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.check_password)
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6474;
                color: white;
                padding: 6px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #bb6474;
            }
        """)

        # 设置布局
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20, 40, 20, 20)  # 增加上方间距，避免按钮被遮挡
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.ok_button)

        self.correct_password = "chengang"
        self.ok_button.setDefault(True)
        # self.input.returnPressed.connect(self.ok_button.click)

    def check_password(self):
        if self.input.text() == self.correct_password:
            self.accept()
        else:
            QMessageBox.warning(self, "错误", "密码错误，请重试")

    def mousePressEvent(self, event):
        if event.pos().y() < 30:  # 判断鼠标是否在标题栏区域
            self._is_dragging = True
            self._start_pos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.move(event.globalPos() - self._start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._is_dragging = False
        event.accept()
