"""
main 包初始化模块

导出常用组件方便外部引用：
from src.main import create_app, config
"""

from .app import create_app
from .config import Config

__all__ = ['create_app', 'Config']