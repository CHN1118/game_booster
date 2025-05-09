import json

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from utils import load_config, save_config

class SettingsWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.editor = QTextEdit()
        self.save_btn = QPushButton("保存并返回")
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

        self.config = load_config()  # 加载配置
        self.editor.setText(self.to_pretty_json(self.config))
        self.save_btn.clicked.connect(self.save_and_back)

    def load_config_data(self):
        self.config = load_config()
        self.editor.setText(self.to_pretty_json(self.config))

    def to_pretty_json(self, config):
        import json
        return json.dumps(config, ensure_ascii=False, indent=4)

    def save_and_back(self):
        try:
            config = json.loads(self.editor.toPlainText())  # 尝试解析 JSON
            save_config(config)  # 保存配置
            self.stacked_widget.widget(0).config = config  # 更新主界面配置
            self.stacked_widget.widget(0).populate_games()  # 刷新游戏列表
            self.stacked_widget.setCurrentIndex(0)  # 回到主界面
        except json.JSONDecodeError:
            self.editor.setPlainText("JSON 格式错误，请检查后再保存")