
from http import HTTPStatus


def test_health_check_response(client):
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}
