from datetime import datetime, timezone
import logging

import requests


class LoggingMonitoringHandler(logging.Handler):
    """
    Logging handler that posts log records to a monitoring microservice via HTTP.

    The handler sends a small JSON payload with the level, message and metadata.
    It should never raise exceptions to avoid interfering with application flow.
    """

    def __init__(self, url: str, timeout: float = 2.0) -> None:
        super().__init__()
        self.url = url
        self.timeout = timeout

    def emit(self, record: logging.LogRecord) -> None:
        try:
            payload = {
                "logger": record.name,
                "level": record.levelname,
                "message": self.format(record),
                "time": datetime.now(timezone.utc).isoformat(),
            }

            requests.post(self.url, json=payload, timeout=self.timeout)
        except Exception as e:
            logging.error("Failed to post log to monitoring service: %s", e)

__all__ = ["LoggingMonitoringHandler"]
