#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工具函数模块
"""

import logging
import sys
from typing import Optional

from src.main.config import Config


def setup_logging(
        level: str = "INFO",
        log_format: Optional[str] = None
) -> logging.Logger:
    """
    设置日志配置
    
    Args:
        level: 日志级别
        log_format: 日志格式
    
    Returns:
        logging.Logger: 配置好的logger实例
    """
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # 获取配置
    config = Config()

    # 创建logger
    logger = logging.getLogger(config.PROJECT_NAME)
    logger.setLevel(level)

    # 创建控制台处理器
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # 设置格式
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(handler)

    return logger


def is_valid_email(email: str) -> bool:
    """
    验证邮箱格式是否正确
    
    Args:
        email: 待验证的邮箱地址
    
    Returns:
        bool: 是否是有效的邮箱地址
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    
    Args:
        filename: 文件名
    
    Returns:
        str: 文件扩展名
    """
    import os
    return os.path.splitext(filename)[1]
