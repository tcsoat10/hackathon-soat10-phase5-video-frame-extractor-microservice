
from abc import ABC, abstractmethod

class IZipperGateway(ABC):
    @abstractmethod
    def send_video_to_zipper(self, video_process_result: dict):
        pass

__all__ = ["IZipperGateway"]
