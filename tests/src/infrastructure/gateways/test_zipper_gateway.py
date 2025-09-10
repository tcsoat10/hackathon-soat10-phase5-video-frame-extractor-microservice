from unittest.mock import Mock, patch
import pytest
import requests
from src.infrastructure.gateways.zipper_gateway import ZipperServiceGateway

@patch("src.infrastructure.gateways.zipper_gateway.requests.post")
def test_send_video_to_zipper_success(mock_post):
    gateway = ZipperServiceGateway()
    gateway.zipper_service_url = "http://zipper"
    video = {"job_ref": "abc123"}

    mock_response = mock_post.return_value
    mock_response.raise_for_status = Mock()  # no exception
    mock_response.json.return_value = {"job_id": "job-1"}

    result = gateway.send_video_to_zipper(video)

    mock_post.assert_called_once_with("http://zipper/schedule", json=video)
    assert result == {"job_id": "job-1"}

@patch("src.infrastructure.gateways.zipper_gateway.requests.post")
def test_send_video_to_zipper_failure_raises(mock_post):
    gateway = ZipperServiceGateway()
    gateway.zipper_service_url = "http://zipper"
    video = {"job_ref": "fail-me"}

    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("bad")

    with pytest.raises(requests.exceptions.HTTPError):
        gateway.send_video_to_zipper(video)

@patch("src.infrastructure.gateways.zipper_gateway.requests.post")
def test_send_video_logs_info_on_success(mock_post):
    gateway = ZipperServiceGateway()
    gateway.zipper_service_url = "http://zipper"
    gateway.logger = Mock()
    video = {"job_ref": "abc123"}

    mock_response = mock_post.return_value
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"job_id": "job-1"}

    result = gateway.send_video_to_zipper(video)

    mock_post.assert_called_once_with("http://zipper/schedule", json=video)
    gateway.logger.info.assert_called_once()
    assert "abc123" in gateway.logger.info.call_args[0][0]
    assert result == {"job_id": "job-1"}

@patch("src.infrastructure.gateways.zipper_gateway.requests.post")
def test_send_video_logs_error_on_failure(mock_post):
    gateway = ZipperServiceGateway()
    gateway.zipper_service_url = "http://zipper"
    gateway.logger = Mock()
    video = {"job_ref": "fail-me"}

    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.Timeout("timeout")

    with pytest.raises(requests.exceptions.Timeout):
        gateway.send_video_to_zipper(video)

    mock_post.assert_called_once_with("http://zipper/schedule", json=video)
    gateway.logger.error.assert_called_once()
    assert "Error sending video process result to Zipper Service" in gateway.logger.error.call_args[0][0]

@patch("src.infrastructure.gateways.zipper_gateway.ZIPPER_SERVICE_URL", "http://default-zipper")
@patch("src.infrastructure.gateways.zipper_gateway.requests.post")
def test_send_video_uses_default_config_url(mock_post):
    gateway = ZipperServiceGateway()
    video = {"job_ref": "cfg"}

    mock_response = mock_post.return_value
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"job_id": "job-cfg"}

    result = gateway.send_video_to_zipper(video)

    mock_post.assert_called_once_with("http://default-zipper/schedule", json=video)
    assert result == {"job_id": "job-cfg"}

