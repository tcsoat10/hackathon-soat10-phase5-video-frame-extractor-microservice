import requests
import logging
from src.core.ports.gateways.zipper.i_zipper_gateway import IZipperGateway
from src.config.settings import ZIPPER_SERVICE_URL

class ZipperServiceGateway(IZipperGateway):
    def __init__(self):
        self.zipper_service_url = ZIPPER_SERVICE_URL
        self.logger = logging.getLogger(__name__)

    def send_video_to_zipper(self, video_process_result: dict):
        try:
            response = requests.post(f"{self.zipper_service_url}/schedule", json=video_process_result)
            response.raise_for_status()
            self.logger.info(f"Successfully sent video process result to Zipper Service: {video_process_result.get('job_ref')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending video process result to Zipper Service: {e}")
            raise

__all__ = ["ZipperServiceGateway"]
