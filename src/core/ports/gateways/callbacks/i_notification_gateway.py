from abc import ABC, abstractmethod

from src.core.domain.dtos.callbacks.notification_dto import NotificationDTO


class INotificationGateway(ABC):
    @abstractmethod
    def send_notification(self, notify_url: str, notification_dto: NotificationDTO):
        pass

__all__ = ["INotificationGateway"]
