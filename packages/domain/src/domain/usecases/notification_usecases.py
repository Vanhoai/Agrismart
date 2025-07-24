from abc import ABC, abstractmethod


class PushNotificationUseCase(ABC):
    @abstractmethod
    def send_notification(self, message: str, recipient: str) -> None: ...
