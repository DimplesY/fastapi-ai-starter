from .celery import app


@app.task
def add(x, y):
    print("计算加法")
    return x + y
