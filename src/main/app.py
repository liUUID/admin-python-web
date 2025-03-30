#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主应用模块
"""

import os
from dotenv import load_dotenv
from src.main.config import Config
from src.main.utils.logger import setup_logging, log


def create_app():
    """应用工厂函数"""
    # 初始化基础组件
    load_dotenv()
    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
    log.info("初始化日志-SUCCESS")
    config = Config()
    log.info("初始化配置-SUCCESS")
    log.info(f"当前环境: {'开发环境' if config.is_development() else '生产环境'}")
    # 初始化数据库
    log.info(f"数据库连接: {config.get_database_url()}")
    return Application(config)


class Application:
    """主应用类"""
    def __init__(self, config):
        self.config = config

    def run(self):
        """运行主逻辑"""
        log.info("程序启动")