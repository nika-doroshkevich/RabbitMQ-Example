from aio_pika import IncomingMessage
from aio_pika import connect_robust


async def process_message(message: IncomingMessage):
    async with message.process():
        print("**" * 20)
        print(f"Received message: {message.body.decode()}")
        print("**" * 20)


async def consume():
    connection = await connect_robust("amqp://admin:admin@localhost/")
    channel = await connection.channel()

    queue = await channel.declare_queue("my_queue", durable=True)
    await queue.consume(process_message)
