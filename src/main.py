from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic - Attach to app instance
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = mongo_conn[settings.MONGODB_DATABASE]


    yield  # Application runs here

    # Shutdown logic
    app.mongo_conn.close()

# Instantiate FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(base.base_router)
app.include_router(data.data_router)