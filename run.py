#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
项目启动入口（生产环境使用）
"""

from src.main.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()