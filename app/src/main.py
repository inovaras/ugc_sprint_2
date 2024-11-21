import uvicorn
import logging

from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.db import mongo
from src.core.config import settings
from src.core.logger import LOGGING
from src.api.v1 import ratings, ping

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.mongo = AsyncIOMotorClient(settings.mongo.url)
    yield

app = FastAPI(
    lifespan=lifespan,
    version="0.0.1",
    title=settings.project_name,
    description=settings.project_description,
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(ratings.router, prefix="/api/v1/ratings", tags=["ratings"])
app.include_router(ping.router, prefix="/api/v1/ping", tags=["ping"])

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=settings.default_host,
        port=settings.default_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )