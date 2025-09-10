
import pytest
from unittest.mock import Mock

from src.core.application.use_cases.send_video_to_zipper_use_case import SendVideoToZipperUseCase
from src.core.ports.gateways.zipper.i_zipper_gateway import IZipperGateway


@pytest.fixture
def mock_zipper_gateway():
    return Mock(spec=IZipperGateway)


@pytest.fixture
def send_video_to_zipper_use_case(mock_zipper_gateway):
    return SendVideoToZipperUseCase(zipper_gateway=mock_zipper_gateway)


def test_build_send_video_to_zipper_use_case(mock_zipper_gateway):
    use_case = SendVideoToZipperUseCase.build(zipper_gateway=mock_zipper_gateway)

    assert isinstance(use_case, SendVideoToZipperUseCase)
    assert use_case._zipper_gateway == mock_zipper_gateway


def test_execute_send_video_to_zipper_use_case(send_video_to_zipper_use_case, mock_zipper_gateway):
    video_process_result = {
        "job_ref": "test_job_ref",
        "client_identification": "test_client",
        "bucket": "test_bucket",
        "frames_path": "test_frames_path",
        "notify_url": "http://test.com/notify",
    }

    send_video_to_zipper_use_case.execute(video_process_result)

    mock_zipper_gateway.send_video_to_zipper.assert_called_once_with(video_process_result)
