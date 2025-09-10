
from src.core.ports.gateways.zipper.i_zipper_gateway import IZipperGateway


class SendVideoToZipperUseCase:
    def __init__(self, zipper_gateway: IZipperGateway):
        self._zipper_gateway: IZipperGateway = zipper_gateway

    @classmethod
    def build(cls, zipper_gateway: IZipperGateway) -> "SendVideoToZipperUseCase":
        return cls(zipper_gateway)

    def execute(self, video_process_result: dict):
        self._zipper_gateway.send_video_to_zipper(video_process_result)

__all__ = ["SendVideoToZipperUseCase"]
