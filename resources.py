import os
import sys


def resource_path(relative_path):
    """获取资源路径，支持打包后的资源路径"""
    try:
        base_path = sys._MEIPASS  # 对应 PyInstaller 打包后的路径
    except Exception:
        base_path = os.path.abspath(".")  # 默认使用当前工作目录
    return os.path.join(base_path, relative_path)