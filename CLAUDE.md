# CLAUDE.md

Этот файл предоставляет руководство для Claude Code при работе с кодом в этом репозитории.

# Документация

Описание приложения: docs/app_brd.md
Технический дизайн: docs/app_tech_design.md
План разработки: docs/app_build_plan.md

# Архитектура проекта

**PsyAI** — веб-приложение для кабинета психолога с интеграцией FastAPI и Flask:

## Стек технологий
- **FastAPI** — REST API (OAuth2PasswordBearer, Pydantic)
- **Flask + Jinja2** — серверный рендеринг страниц, сессии, CSRF-защита
- **PostgreSQL** — реляционная БД (хост `db.mironenko.org`, пользователь `psyai_user`)
- **SQLAlchemy + Alembic** — ORM и миграции
- **PyJWT** — токены доступа (срок 30 минут)
- **bcrypt** — хеширование паролей

## Структура проекта
```
psyai_app/
├── app/              # FastAPI
│   ├── main.py       #主应用入口
│   └── routers/      # API роутеры (auth, users, admin, sessions)
├── flask_app/        # Flask приложение
│   ├── main.py       # Flask + Jinja2
│   └── templates/    # HTML шаблоны
├── alembic/          # миграции БД
└── tests/
```

## Ключевые эндпоинты

**Auth:**
- `POST /api/auth/login` — вход, возвращает JWT
- `POST /api/auth/register` — регистрация
- `POST /api/auth/reset-password` — восстановление пароля

**Users:**
- `GET /api/users/me` — текущий пользователь
- `PUT/PATCH /api/users/me/profile` — обновление профиля
- `DELETE /api/users/deactivate` — деактивация аккаунта

**Admin:**
- `CRUD /api/admin/users` — управление пользователями
- `CRUD /api/admin/plans` — управление планами доступа
- `GET /api/admin/stats` — статистика

## Интеграция Flask ↔ FastAPI
- Flask использует `httpx` для запросов к FastAPI
- JWT передаётся в заголовке `Authorization: Bearer <token>`
- Переменная окружения `API_URL` указывает на FastAPI сервис

## Планы доступа
- `0` — free
- `1` — basic
- `2` — premium
- `3` — ultra

## Переменные окружения
- `DATABASE_URL` — подключение к PostgreSQL
- `SECRET_KEY` / `FLASK_SECRET_KEY` — ключи шифрования
- `API_URL` — URL FastAPI сервиса

## Разработка
```bash
# Установка зависимостей (после создания requirements.txt)
pip install -r requirements.txt

# Запуск миграций
alembic upgrade head

# Запуск тестов
pytest

# Форматирование
black .
isort .

# Линтинг (pre-commit)
pre-commit run --all-files
```
