import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog

from ui_main import MainWindow
from ui_settings import SettingsWindow
from password_dialog import PasswordDialog


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("小橙子")
        self.setWindowIcon(QIcon("./app_icon.ico"))  # 设置任务栏图标
        self.setFixedSize(600, 500)

        # 创建 QStackedWidget 并添加页面
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        main_window = MainWindow(self.stack)
        settings_window = SettingsWindow(self.stack)

        self.stack.addWidget(main_window)
        self.stack.addWidget(settings_window)
        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置应用程序图标（双保险）
    icon = QIcon("./app_icon.ico")
    print(icon.isNull())  # False 表示图标已加载
    app.setWindowIcon(icon)

    # 密码验证弹窗
    # dialog = PasswordDialog()
    # if dialog.exec_() != QDialog.Accepted:
    #     sys.exit()

    # 启动主程序窗口
    window = MainApp()
    window.show()

    sys.exit(app.exec_())
