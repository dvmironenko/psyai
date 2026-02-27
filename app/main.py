"""Основной модуль FastAPI приложения."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import config
from .routers import auth, users, admin

# Создание FastAPI приложения
app = FastAPI(
    title="PsyAI API",
    description="API для кабинета психолога с интеграцией Flask",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене уточнить список origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "PsyAI API v1.0.0"}


@app.get("/health")
async def health_check():
    """Проверка здоровья API."""
    return {"status": "ok"}


# Подключение роутеров
app.include_router(auth.router, prefix=f"{config.API_V1_PREFIX}/auth", tags=["Auth"])
app.include_router(users.router, prefix=f"{config.API_V1_PREFIX}/users", tags=["Users"])
app.include_router(admin.router, prefix=f"{config.API_V1_PREFIX}/admin", tags=["Admin"])
