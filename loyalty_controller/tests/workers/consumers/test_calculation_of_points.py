import json

from src.common.utils import calculate_percentages


async def test_calculation_of_points_ok(
    monkeypatch,
    calculation_of_points_service,
    mock_loyalty_api_ok,
):
    user_id = "f51f3683-7758-402e-9cf4-785f840d8738"
    amount = 600
    message = {"user_id": user_id, "amount": amount}
    bytes_string = json.dumps(message).encode("utf-8")
    loyalty_level = 5
    points = calculate_percentages(loyalty_level, amount)

    amqp_message = {}
    amqp_routing_key = None

    async def mock_callback(*args, **kwargs):
        nonlocal amqp_message
        nonlocal amqp_routing_key
        amqp_message = kwargs.get("message")
        amqp_routing_key = kwargs.get("routing_key")

    monkeypatch.setattr("tests.utils.amqp.MockAMQPSender.send", mock_callback)

    await calculation_of_points_service.main(bytes_string)

    assert amqp_message == dict(user_id=user_id, points=points)
    assert amqp_routing_key == "event.add"
