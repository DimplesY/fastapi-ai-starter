mq_user = "guest"
mq_password = "guest"
broker_url = f"amqp://{mq_user}:{mq_password}@rabbitmq:5672//"
# broker_url = f"amqp://{mq_user}:{mq_password}@localhost:5672//"
result_backend = "redis://:123456@redis:6379/0"
# result_backend = "redis://:123456@localhost:6379/0"
accept_content = ["json", "pickle"]
timezone = "Asia/Shanghai"
enable_utc = False
include = ["celery_tasks.workers.task_01"]
beat_schedule = {
    "add-every-10-seconds": {
        "task": "celery_tasks.workers.task_01.add",
        "schedule": 10.0,
        "args": (16, 16),
    },
}
