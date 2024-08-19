from aio_pika import ExchangeType
from aio_pika import IncomingMessage
from aio_pika import connect_robust


async def process_message(message: IncomingMessage, queue_name: str):
    async with message.process():
        print("**" * 20)
        print(f"Received message from queue: {queue_name}")
        print(f"Message body: {message.body.decode()}")
        print("**" * 20)


async def consume():
    connection = await connect_robust("amqp://admin:admin@localhost/")
    channel = await connection.channel()

    exchange = await channel.declare_exchange("my_headers_exchange", ExchangeType.HEADERS)

    queue1 = await channel.declare_queue("queue_1_test_headers", durable=True)
    queue2 = await channel.declare_queue("queue_2_test_headers", durable=True)

    await queue1.bind(
        exchange,
        arguments={"x-match": "any", "header_key": "value_a"}
    )
    await queue2.bind(
        exchange,
        arguments={"x-match": "any", "header_key": "value_b"}
    )

    async def wrapper_process_message(message: IncomingMessage):
        header_value = message.headers.get("header_key")
        if header_value == "value_a":
            await process_message(message, "queue_1_test_headers")
        elif header_value == "value_b":
            await process_message(message, "queue_2_test_headers")

    await queue1.consume(wrapper_process_message)
    await queue2.consume(wrapper_process_message)
