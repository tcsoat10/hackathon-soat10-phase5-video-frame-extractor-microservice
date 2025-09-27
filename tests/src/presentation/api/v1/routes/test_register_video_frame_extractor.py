from http import HTTPStatus
from unittest.mock import patch

from tests.conftest import get_headers


def test_send_empty_payload_for_route_register_video(client):
    response = client.post("/api/v1/video/register")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["query", "client_identification"],
                "msg": "Field required",
                "type": "missing"
            },
            {
                "input": None,
                "loc": ["body", "video_file"],
                "msg": "Field required",
                "type": "missing"
            }
        ]
    }

# Mock upload_object and enqueue_video_processing_task
@patch('src.infrastructure.gateways.s3_storage_gateway.S3StorageGateway.upload_object')
@patch('src.infrastructure.gateways.celery_task_queue_gateway.CeleryTaskQueueGateway.enqueue_video_processing_task')
def test_send_correct_payload_for_route_register_video(mock_enqueue_task, mock_upload_object, client):
    mock_enqueue_task.return_value = "mocked_task_id"
    mock_upload_object.return_value = {"message": "Object uploaded successfully"}
    
    response = client.post(
        "/api/v1/video/register",
        params={"client_identification": "test_client", "notify_url": "http://callback.url"},
        files={"video_file": ("test_video.mp4", b"fake video content", "video/mp4")},
        headers=get_headers()
    )
    assert response.status_code == HTTPStatus.CREATED
    
    response_json = response.json()
    assert 'id' in response_json
    assert 'job_ref' in response_json
    assert 'status' in response_json
    assert 'created_at' in response_json
    assert 'updated_at' in response_json
    assert response_json['status'] == 'QUEUED'
