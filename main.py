import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog

from ui_main import MainWindow
from ui_settings import SettingsWindow
from password_dialog import PasswordDialog


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("助力助手")
        self.setWindowIcon(QIcon("./app_icon.ico"))  # 设置任务栏图标

        # 移除固定大小设置，改为设置初始大小
        self.resize(800, 600)  # 初始大小

        # 允许窗口最小化和最大化
        self.setMinimumSize(800, 600)  # 设置最小尺寸（可选）
        # self.setMaximumSize(800, 600)  # 如果要限制最大尺寸可以取消注释

        # 启用窗口大小调整（默认就是启用的，这行可以省略）
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.MSWindowsFixedSizeDialogHint)

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
