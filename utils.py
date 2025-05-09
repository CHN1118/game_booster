import json
import os
import sys

from pathlib import Path  # 更现代的路径处理

CONFIG_NAME = "config.json"


def get_config_path():
    """获取配置文件路径（确保始终返回用户可写的路径）"""
    if getattr(sys, 'frozen', False):
        # 打包后：保存到exe所在目录（确保可写）
        return Path(sys.executable).parent / CONFIG_NAME
    else:
        # 开发模式：保存到项目根目录
        return Path(__file__).parent / CONFIG_NAME


def load_config():
    """加载配置（优先用户修改的配置，不存在则读取默认配置）"""
    config_path = get_config_path()
    default_path = Path(__file__).parent / CONFIG_NAME  # 默认配置（开发/打包后都在资源中）

    # 1. 尝试读取用户配置
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"配置文件损坏: {e}")

    # 2. 尝试读取默认配置
    if default_path.exists():
        try:
            with open(default_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"默认配置文件损坏: {e}")

    # 3. 返回空配置并生成文件
    default_config = {"version": 1, "settings": {}}
    save_config(default_config)  # 自动创建初始文件
    return default_config


def save_config(config):
    """保存配置（自动处理路径和权限）"""
    config_path = get_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"保存配置失败: {e}")
        # 尝试保存到用户目录作为备用方案
        user_path = Path.home() / f".{CONFIG_NAME}"
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print(f"已保存到备用路径: {user_path}")