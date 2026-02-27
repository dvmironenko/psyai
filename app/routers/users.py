"""Роутер пользователей."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..auth import get_current_active_user
from ..database import get_db
from ..models import User

router = APIRouter()


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Получить информацию о текущем пользователе."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin,
        "plan_id": current_user.plan_id,
    }


@router.put("/me/profile")
def update_profile(
    email: Optional[str] = None,
    password: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Обновить профиль текущего пользователя."""
    if email is not None:
        existing_user = db.query(User).filter(User.email == email, User.id != current_user.id).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )
        current_user.email = email

    if password is not None:
        from ..auth import get_password_hash
        current_user.password_hash = get_password_hash(password)

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
        },
    }


@router.delete("/deactivate")
def deactivate_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Деактивировать аккаунт."""
    current_user.is_active = False
    db.commit()

    return {"message": "Account deactivated successfully"}
