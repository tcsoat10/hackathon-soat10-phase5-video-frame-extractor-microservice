import requests
import logging
from src.core.ports.gateways.zipper.i_zipper_gateway import IZipperGateway
from src.config.settings import ZIPPER_SERVICE_URL, ZIPPER_SERVICE_X_API_KEY

class ZipperServiceGateway(IZipperGateway):
    def __init__(self):
        self.zipper_service_url = ZIPPER_SERVICE_URL
        self.zipper_service_x_api_key = ZIPPER_SERVICE_X_API_KEY
        self.logger = logging.getLogger(__name__)

    def send_video_to_zipper(self, video_process_result: dict):
        try:
            response = requests.post(
                f"{self.zipper_service_url}/zip/register",
                json=video_process_result,
                headers={"x-api-key": self.zipper_service_x_api_key}
            )
            response.raise_for_status()
            self.logger.info(f"Successfully sent video process result to Zipper Service: {video_process_result.get('job_ref')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending video process result to Zipper Service: {e}")
            raise

__all__ = ["ZipperServiceGateway"]
