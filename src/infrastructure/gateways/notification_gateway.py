import requests
import logging

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.core.domain.dtos.callbacks.notification_dto import NotificationDTO
from src.core.ports.gateways.callbacks.i_notification_gateway import INotificationGateway


class NotificationGateway(INotificationGateway):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def send_notification(self, notify_url: str, notification_dto: NotificationDTO):
        if not notify_url:
            self.logger.info(f"No notify_url provided for job_ref {notification_dto.job_ref}. Skipping notification.")
            return

        try:
            response = requests.post(notify_url, json=notification_dto.model_dump())
            print(f"Response: {response.text}")
            response.raise_for_status()
            self.logger.info(f"Notification sent successfully for job_ref {notification_dto.job_ref} to {notify_url}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send notification for job_ref {notification_dto.job_ref} to {notify_url}: {e}")

__all__ = ["NotificationGateway"]
