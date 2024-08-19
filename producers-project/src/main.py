from fastapi import FastAPI

from test_rabbitmq.direct_rabbitmq import router as direct_rabbitmq_router
from test_rabbitmq.fanout_rabbitmq import router as fanout_exchange_router
from test_rabbitmq.headers_rabbitmq import router as headers_exchange_router
from test_rabbitmq.test_rabbitmq import router as test_rabbitmq_router
from test_rabbitmq.topic_rabbitmq import router as topic_exchange_router

app = FastAPI(
    title="App"
)

app.include_router(test_rabbitmq_router)
app.include_router(direct_rabbitmq_router)
app.include_router(fanout_exchange_router)
app.include_router(topic_exchange_router)
app.include_router(headers_exchange_router)
