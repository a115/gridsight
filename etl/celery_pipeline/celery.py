from celery import Celery

from app.configuration.celery import celery_settings

etl_app = Celery(
    main="GridSight",
    broker=celery_settings.broker_url,
    backend=celery_settings.result_backend,
)

etl_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

etl_app.autodiscover_tasks()
