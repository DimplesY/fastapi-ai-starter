from celery_tasks.celery import celery_app as app


@app.task
def add(x, y):
    print("计算加法")
    return x + y
