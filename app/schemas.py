"""Pydantic схемы для валидации."""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserPlanBase(BaseModel):
    """Базовая схема плана."""
    id: int
    name: str
    description: str | None = None


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    plan_id: int = 0


class UserCreate(UserBase):
    """Схема для создания пользователя."""
    password: str


class UserUpdate(BaseModel):
    """Схема для обновления пользователя."""
    email: EmailStr | None = None
    password: str | None = None
    plan_id: int | None = None


class User(UserBase):
    """Схема пользователя с ID."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Схема токена доступа."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Схемаpayload токена."""
    sub: int  # user id


class Message(BaseModel):
    """Схема сообщения."""
    message: str
