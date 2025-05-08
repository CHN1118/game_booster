import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from ui_main import MainWindow
from ui_settings import SettingsWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked = QStackedWidget() # 创建堆栈窗口
    main_window = MainWindow(stacked) # 创建主界面
    settings_window = SettingsWindow(stacked) # 创建设置界面

    stacked.addWidget(main_window)  # 添加主界面到堆栈窗口
    stacked.addWidget(settings_window) # 添加设置界面到堆栈窗口

    stacked.setFixedSize(600, 500) # 设置窗口大小
    stacked.setCurrentIndex(0)  # 显示主界面
    stacked.show() # 显示窗口

    sys.exit(app.exec_()) # 运行程序
