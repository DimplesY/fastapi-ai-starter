broker_url = "redis://:123456@redis:6379/1"
# broker_url = "redis://:123456@localhost:6379/1"
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
