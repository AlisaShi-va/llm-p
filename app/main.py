from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine  # Будет создан в слое app/db/session.py
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Действия при старте
    async with engine.begin() as conn:
        # Генерация таблиц в SQLite
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    """Сборка и конфигурации FastAPI"""
    application = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение эндпоинтов
    application.include_router(auth_router, prefix="/api/v1")
    application.include_router(chat_router, prefix="/api/v1")

    # Health check (тех.эндпоинт)
    @application.get("/health", tags=["Infrastructure"], status_code=200)
    async def health_check():
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "app_name": settings.APP_NAME
        }

    return application

app = create_app()
