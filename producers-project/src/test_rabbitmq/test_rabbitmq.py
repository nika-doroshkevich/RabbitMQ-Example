from aio_pika import Message
from aio_pika import connect_robust
from fastapi import APIRouter
from fastapi import BackgroundTasks

router = APIRouter(prefix="/test-rabbitmq")


async def get_rabbitmq_connection():
    return await connect_robust("amqp://admin:admin@localhost/")


async def send_message(message: str):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("my_queue", durable=True)
        await channel.default_exchange.publish(
            Message(body=message.encode()),
            routing_key=queue.name
        )


@router.post("/send")
async def send(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message)
    return {"status": "Message sent"}
