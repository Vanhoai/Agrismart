from celery import Celery
from .tasks import *

broker = "amqp://hinsun:hinsun@localhost:5672/"
app = Celery("AgrismartQueue", broker=broker)

app.conf.update(
    task_routes={
        "agrismart.queues.tasks.notification.*": {"queue": "notification"},
    },
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

app.autodiscover_tasks()
