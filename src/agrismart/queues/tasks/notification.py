import time
from celery import shared_task


@shared_task
def send_push_notification(msg: str):
    print("Sending push notification...")
    for i in range(1, 5):
        time.sleep(3)
        print(f"Push notification {i} sent: {msg}")
