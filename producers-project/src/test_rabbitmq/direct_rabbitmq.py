from aio_pika import ExchangeType
from aio_pika import Message
from aio_pika import connect_robust
from fastapi import APIRouter
from fastapi import BackgroundTasks

router = APIRouter(prefix="/test-direct-exchange")


async def get_rabbitmq_connection():
    return await connect_robust("amqp://admin:admin@localhost/")


async def send_message(message: str):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange("my_direct_exchange", ExchangeType.DIRECT)

        queue1 = await channel.declare_queue("queue_1_test_direct", durable=True)
        queue2 = await channel.declare_queue("queue_2_test_direct", durable=True)

        await queue1.bind(exchange, routing_key="my_routing_key")
        await queue2.bind(exchange, routing_key="my_routing_key2")

        str_len = len(message)
        if str_len <= 10:
            routing_key = "my_routing_key"
        else:
            routing_key = "my_routing_key2"

        await exchange.publish(
            Message(body=message.encode()),
            routing_key=routing_key
        )


@router.post("/send")
async def send(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message)
    return {"status": "Message sent"}
