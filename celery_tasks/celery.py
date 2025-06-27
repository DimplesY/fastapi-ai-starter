from celery import Celery


def make_celery(app_name: str, config: str) -> Celery:
    app = Celery(app_name)
    app.config_from_object(config)
    return app


celery_app = make_celery("celery_tasks", "celery_tasks.celeryconfig")
