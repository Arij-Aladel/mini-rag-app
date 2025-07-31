from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

from stores.LLMProviderFactory import LLMProviderFactory
from stores.LLMEnums import LLMEnums

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic - Attach to app instance
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    llm_privider_factory = LLMProviderFactory(settings)

    #generate LLM client based on settings
    app.generation.client = llm_privider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation.client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    #embedding LLM client
    app.embedding.client = llm_privider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding.client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_SIZE)
    yield  # Application runs here

    # Shutdown logic
    app.mongo_conn.close()

# Instantiate FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(base.base_router)
app.include_router(data.data_router)