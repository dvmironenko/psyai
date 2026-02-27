"""Настройка базы данных и сессий."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import config

# Engine для подключения к PostgreSQL
engine = create_engine(
    config.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

# SessionLocal для создания сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """Получить сессию базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
