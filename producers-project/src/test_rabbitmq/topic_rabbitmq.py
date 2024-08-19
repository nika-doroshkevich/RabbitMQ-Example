from aio_pika import ExchangeType
from aio_pika import Message
from aio_pika import connect_robust
from fastapi import APIRouter
from fastapi import BackgroundTasks

router = APIRouter(prefix="/test-topic-exchange")


async def get_rabbitmq_connection():
    return await connect_robust("amqp://admin:admin@localhost/")


async def send_message(message: str):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange("my_topic_exchange", ExchangeType.TOPIC)

        queue1 = await channel.declare_queue("queue_1_test_topic", durable=True)
        queue2 = await channel.declare_queue("queue_2_test_topic", durable=True)

        await queue1.bind(exchange, routing_key="a.info")
        await queue2.bind(exchange, routing_key="b.info")

        str_len = len(message)
        if str_len <= 10:
            routing_key = "a.info"
        else:
            routing_key = "b.info"

        await exchange.publish(
            Message(body=message.encode()),
            routing_key=routing_key
        )


@router.post("/send")
async def send(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message)
    return {"status": "Message sent"}
