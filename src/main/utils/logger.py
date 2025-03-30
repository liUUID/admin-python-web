#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志配置模块（支持全局访问）
"""

import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

# 全局日志对象
_global_logger = None


def create_file_handler(
        filename: str,
        level: int,
        formatter: logging.Formatter,
        backup_count: int = 60,
        filter_func: Optional[Callable] = None,
        encoding: str = "utf-8"
) -> logging.handlers.TimedRotatingFileHandler:
    """
    创建文件处理器（修复版）
    """
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(filename),
        when="midnight",
        interval=1,
        backupCount=backup_count,
        encoding=encoding
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)

    if filter_func:
        handler.addFilter(filter_func)

    return handler


def setup_logging(level="INFO") -> logging.Logger:
    """
    设置日志配置（修复版）
    """
    global _global_logger

    if _global_logger is not None:
        return _global_logger

    # 创建logs目录
    log_path = Path("./logs")
    log_path.mkdir(exist_ok=True)

    # 创建logger
    logger = logging.getLogger("admin")
    logger.setLevel(level)

    # 关键修复：确保handler创建成功
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)s] %(levelname)s %(name)s - %(message)s"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        # 文件处理器
        file_handlers = [
            create_file_handler(
                str(log_path / "sys-console.log"),
                logging.INFO,
                formatter
            ),
            create_file_handler(
                str(log_path / "sys-info.log"),
                logging.INFO,
                formatter,
                filter_func=lambda r: r.levelno == logging.INFO
            ),
            create_file_handler(
                str(log_path / "sys-error.log"),
                logging.ERROR,
                formatter,
                filter_func=lambda r: r.levelno == logging.ERROR
            )
        ]

        for handler in file_handlers:
            if handler:  # 确保handler不是None
                logger.addHandler(handler)

    except Exception as e:
        print(f"无法创建文件处理器: {str(e)}")
        # 至少保证控制台日志可用

    _global_logger = logger
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    获取全局日志对象
    """
    if _global_logger is None:
        setup_logging()  # 默认初始化
    return _global_logger if name is None else logging.getLogger(f"admin.{name}")


# 全局日志对象
log = get_logger()