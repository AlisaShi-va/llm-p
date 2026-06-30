from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Общие настройки приложения
    APP_NAME: str = "LLM Gateway API"
    ENVIRONMENT: str = "development"

    # Настройки JWT безопасности
    JWT_SECRET_KEY: str = Field(..., alias="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Настройки Базы Данных (SQLite)
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # Настройки OpenRouter
    OPENROUTER_API_KEY: str = Field(..., alias="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai"
    OPENROUTER_MODEL: str = "meta-llama/llama-3-8b-instruct:free"
    OPENROUTER_REFERER: str = "https://github.com"
    OPENROUTER_TITLE: str = "LLM Gateway App"

    # Конфигурация парсинга .env файла
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
