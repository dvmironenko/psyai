"""Роутер администратора."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..auth import get_current_admin
from ..database import get_db
from ..models import User, UserPlan

router = APIRouter()


# CRUD для пользователей
@router.get("/users")
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Получить список всех пользователей."""
    users = db.query(User).offset(skip).limit(limit).all()
    return {
        "items": [
            {"id": u.id, "email": u.email, "is_active": u.is_active, "plan_id": u.plan_id}
            for u in users
        ],
        "total": db.query(User).count(),
    }


@router.get("/users/{user_id}")
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Получить пользователя по ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    email: Optional[str] = None,
    password: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    plan_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Обновить пользователя по ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if email is not None:
        user.email = email
    if password is not None:
        from ..auth import get_password_hash
        user.password_hash = get_password_hash(password)
    if is_active is not None:
        user.is_active = is_active
    if is_admin is not None:
        user.is_admin = is_admin
    if plan_id is not None:
        user.plan_id = plan_id

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user_id": user.id}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Удалить пользователя по ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully", "user_id": user_id}


# CRUD для планов
@router.get("/plans")
def read_plans(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    """Получить список всех планов."""
    plans = db.query(UserPlan).all()
    return {"items": plans, "total": len(plans)}


@router.get("/plans/{plan_id}")
def read_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    """Получить план по ID."""
    plan = db.query(UserPlan).filter(UserPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan


@router.post("/plans")
def create_plan(
    name: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Создать новый план."""
    plan = UserPlan(name=name, description=description)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return {"message": "Plan created successfully", "plan_id": plan.id}


@router.put("/plans/{plan_id}")
def update_plan(
    plan_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Обновить план по ID."""
    plan = db.query(UserPlan).filter(UserPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    if name is not None:
        plan.name = name
    if description is not None:
        plan.description = description

    db.commit()
    return {"message": "Plan updated successfully", "plan_id": plan.id}


@router.delete("/plans/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Удалить план по ID."""
    plan = db.query(UserPlan).filter(UserPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    db.delete(plan)
    db.commit()
    return {"message": "Plan deleted successfully", "plan_id": plan.id}


# Статистика
@router.get("/stats")
def read_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    """Получить статистику."""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_users = db.query(User).filter(User.is_admin == True).count()

    # Планы
    plans = db.query(UserPlan).all()
    plan_counts = {p.name: db.query(User).filter(User.plan_id == p.id).count() for p in plans}

    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "plan_distribution": plan_counts,
    }
