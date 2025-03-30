#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库工具模块
"""

import pymysql
from ..config import Config


def open_db():
    """
    打开数据库连接
    
    Returns:
        pymysql.connections.Connection: 数据库连接对象
    """
    config = Config()
    
    try:
        # 使用配置中的数据库参数创建连接
        db = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            charset='utf8mb4'
        )
        return db
    except pymysql.Error as e:
        raise Exception(f"数据库连接失败: {str(e)}")


def close_db(db):
    """
    关闭数据库连接
    
    Args:
        db: 数据库连接对象
    """
    if db:
        db.close()


def execute_query(sql, params=None):
    """
    执行查询语句
    
    Args:
        sql: SQL查询语句
        params: 查询参数
    
    Returns:
        list: 查询结果
    """
    db = None
    try:
        db = open_db()
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        close_db(db)


def execute_update(sql, params=None):
    """
    执行更新语句
    
    Args:
        sql: SQL更新语句
        params: 更新参数
    
    Returns:
        int: 影响的行数
    """
    db = None
    try:
        db = open_db()
        with db.cursor() as cursor:
            affected_rows = cursor.execute(sql, params)
            db.commit()
            return affected_rows
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        close_db(db)
