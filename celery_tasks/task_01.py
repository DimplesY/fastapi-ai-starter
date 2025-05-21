#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : compose-fastapi 
@File    : task_01.py
@Author  : DimplesY
@Date    : 2025/5/21 15:01 
"""
from .celery import app

@app.task
def add(x, y):
    print('计算加法')
    return x + y
