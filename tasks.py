#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : compose-fastapi 
@File    : tasks.py
@Author  : DimplesY
@Date    : 2025/5/21 15:01 
"""
from celery import Celery

app = Celery("tasks", backend="rpc://", broker="amqp://guest:guest@rabbitmq:5672//")

@app.task
def add(x, y):
    return x + y
