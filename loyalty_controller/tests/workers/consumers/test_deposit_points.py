import json


async def test_deposit_points_ok(
    monkeypatch,
    deposit_points_service,
    mock_loyalty_api_ok,
):
    user_id = "f51f3683-7758-402e-9cf4-785f840d8738"
    points = 100
    message = {"user_id": user_id, "points": points}
    bytes_string = json.dumps(message).encode("utf-8")

    await deposit_points_service.main(bytes_string)
