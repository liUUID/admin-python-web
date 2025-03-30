#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工具函数测试模块
"""

import pytest
from src.main.utils import is_valid_email, get_file_extension

def test_is_valid_email():
    """测试邮箱验证函数"""
    # 有效的邮箱地址
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("user.name@domain.co.uk") == True
    
    # 无效的邮箱地址
    assert is_valid_email("invalid.email") == False
    assert is_valid_email("@domain.com") == False
    assert is_valid_email("user@.com") == False

def test_get_file_extension():
    """测试获取文件扩展名函数"""
    assert get_file_extension("test.txt") == ".txt"
    assert get_file_extension("image.jpg") == ".jpg"
    assert get_file_extension("document") == ""
    assert get_file_extension(".gitignore") == "" 