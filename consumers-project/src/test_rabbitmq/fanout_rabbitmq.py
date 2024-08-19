from aio_pika import ExchangeType
from aio_pika import IncomingMessage
from aio_pika import connect_robust


async def process_message(message: IncomingMessage):
    async with message.process():
        print("**" * 20)
        print(f"Message body: {message.body.decode()}")
        print("**" * 20)


async def consume():
    connection = await connect_robust("amqp://admin:admin@localhost/")
    channel = await connection.channel()

    exchange = await channel.declare_exchange("my_fanout_exchange", ExchangeType.FANOUT)

    queue1 = await channel.declare_queue("queue_1_test_fanout", durable=True)
    queue2 = await channel.declare_queue("queue_2_test_fanout", durable=True)

    await queue1.bind(exchange)
    await queue2.bind(exchange)

    await queue1.consume(process_message)
    await queue2.consume(process_message)
