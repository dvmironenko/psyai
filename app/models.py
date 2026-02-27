"""Модели базы данных."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """Модель пользователя."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    plan_id = Column(Integer, ForeignKey("users_plans.id"), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    plan = relationship("UserPlan", back_populates="users")


class UserPlan(Base):
    """Модель плана доступа."""
    __tablename__ = "users_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    # Relationships
    users = relationship("User", back_populates="plan")
