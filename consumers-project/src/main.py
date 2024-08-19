import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from test_rabbitmq.direct_rabbitmq import consume as direct_rabbitmq_consume
from test_rabbitmq.fanout_rabbitmq import consume as fanout_exchange_consume
from test_rabbitmq.headers_rabbitmq import consume as headers_exchange_consume
from test_rabbitmq.test_rabbitmq import consume as test_rabbitmq_consume
from test_rabbitmq.topic_rabbitmq import consume as topic_exchange_consume

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="App"
)


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup - starting RabbitMQ listener")
    asyncio.create_task(test_rabbitmq_consume())
    asyncio.create_task(direct_rabbitmq_consume())
    asyncio.create_task(fanout_exchange_consume())
    asyncio.create_task(topic_exchange_consume())
    asyncio.create_task(headers_exchange_consume())


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
        reload=True,
    )
