from domain.usecases import PushNotificationUseCase


class NotificationService(PushNotificationUseCase):
    def __init__(self) -> None:
        super().__init__()

    def send_notification(self, message: str, recipient: str) -> None:
        # Logic to send a push notification
        print(f"Push notification sent to {recipient}: {message}")
