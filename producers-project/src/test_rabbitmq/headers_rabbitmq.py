from aio_pika import ExchangeType
from aio_pika import Message
from aio_pika import connect_robust
from fastapi import APIRouter
from fastapi import BackgroundTasks

router = APIRouter(prefix="/test-headers-exchange")


async def get_rabbitmq_connection():
    return await connect_robust("amqp://admin:admin@localhost/")


async def send_message(message: str):
    connection = await get_rabbitmq_connection()
    async with connection:
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

        headers = {"header_key": "value_a"} if len(message) <= 10 else {"header_key": "value_b"}

        await exchange.publish(
            Message(
                body=message.encode(),
                headers=headers
            ),
            routing_key=""
        )


@router.post("/send")
async def send(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message)
    return {"status": "Message sent"}
