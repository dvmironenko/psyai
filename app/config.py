"""Конфигурация приложения."""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Базовая конфигурация."""
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/psyai")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # FastAPI
    API_V1_PREFIX: str = "/api/v1"

    # Flask integration
    API_URL: str = os.getenv("API_URL", "http://localhost:8000")


class DevelopmentConfig(BaseConfig):
    """Конфигурация для разработки."""
    DEBUG: bool = True


class ProductionConfig(BaseConfig):
    """Конфигурация для продакшена."""
    DEBUG: bool = False


def get_config():
    """Получить конфигурацию в зависимости от окружения."""
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()


config = get_config()
