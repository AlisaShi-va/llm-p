from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Создание асинхронного engine
engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Генерация асинхронных сессий БД
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
