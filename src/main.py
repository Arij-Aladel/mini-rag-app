from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import base, data, nlp
from helpers.config import get_settings

from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.llm.LLMEnums import LLMEnums

from stores.vectordb.VectorDBProvidorFactory import VectorDBProvidorFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic - Attach to app instance
    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB_NAME}"
    app.db_engine = create_async_engine(postgres_conn)

    app.db_client = sessionmaker(
        bind=app.db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProvidorFactory(settings)

    #generate LLM client based on settings
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    #embedding LLM client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    #vector database client
    app.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND,
        )

    app.vectordb_client.connect() 

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )


    yield  # Application runs here

    # Shutdown logic
    app.db_engine.dispose()
    app.vectordb_client.disconnect()
    app.generation_client = None
    app.db_client = None

# Instantiate FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)