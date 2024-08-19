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

    exchange = await channel.declare_exchange("my_direct_exchange", ExchangeType.DIRECT)

    queue1 = await channel.declare_queue("queue_1_test_direct", durable=True)
    queue2 = await channel.declare_queue("queue_2_test_direct", durable=True)

    await queue1.bind(exchange, routing_key="my_routing_key")
    await queue2.bind(exchange, routing_key="my_routing_key2")

    async def wrapper_process_message(message: IncomingMessage):
        if message.routing_key == "my_routing_key":
            await process_message(message, "queue_1_test_direct")
        elif message.routing_key == "my_routing_key2":
            await process_message(message, "queue_2_test_direct")

    await queue1.consume(wrapper_process_message)
    await queue2.consume(wrapper_process_message)
