#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import os
from pathlib import Path
from dataclasses import dataclass
import pymysql
from dotenv import load_dotenv


def load_env_file():
    """
    加载环境变量文件
    优先加载.env文件，如果不存在则加载.env.example
    """
    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if env_path.exists():
        load_dotenv(env_path)
    elif env_example_path.exists():
        print("警告: .env 文件不存在，使用 .env.example 作为配置模板")
        load_dotenv(env_example_path)
    else:
        print("警告: 未找到 .env 或 .env.example 文件，使用默认配置")


@dataclass
class Config:
    """配置类"""
    # 项目配置
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "admin-python-web")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "A sample project")

    # 数据库配置
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "liuuid_db")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin123")

    # 应用配置
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API配置
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    def __post_init__(self):
        # 记录配置来源
        self._sources = {
            field: "env" if os.getenv(field) is not None else "default"
            for field in self.__annotations__
        }
        print("配置来源:", self._sources)

        # 验证逻辑
        self._validate_database_config()
        self._validate_api_config()
        self._validate_log_level()

    def _validate_database_config(self):
        """验证数据库配置"""
        # 验证端口号范围
        if not (1 <= self.DB_PORT <= 65535):
            raise ValueError(f"数据库端口号必须在1-65535之间: {self.DB_PORT}")

        # 验证数据库名称
        if not self.DB_NAME or not self.DB_NAME.strip():
            raise ValueError("数据库名称不能为空")

        # 验证数据库连接
        try:
            conn = pymysql.connect(
                host=self.DB_HOST,
                port=self.DB_PORT,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                database=self.DB_NAME,
                connect_timeout=5
            )
            conn.close()
        except pymysql.Error as e:
            raise ValueError(f"数据库连接失败: {str(e)}")

    def _validate_api_config(self):
        """验证API配置"""
        # 验证API端口号范围
        if not (1 <= self.API_PORT <= 65535):
            raise ValueError(f"API端口号必须在1-65535之间: {self.API_PORT}")

        # 验证API主机地址
        if not self.API_HOST:
            raise ValueError("API主机地址不能为空")

    def _validate_log_level(self):
        """验证日志级别"""
        valid_log_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if self.LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError(f"无效的日志级别: {self.LOG_LEVEL}")

    def get_database_url(self) -> str:
        """
        获取数据库URL
        
        Returns:
            str: 数据库连接URL
        """
        return f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def is_development(self) -> bool:
        """
        判断是否为开发环境
        
        Returns:
            bool: 是否为开发环境
        """
        return self.DEBUG

    def is_production(self) -> bool:
        """
        判断是否为生产环境
        
        Returns:
            bool: 是否为生产环境
        """
        return not self.DEBUG




load_env_file()
