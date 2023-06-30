from http import HTTPStatus


async def test_ping(test_client):
    response = await test_client.get("/api/srv/ping")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"result": "pong"}
