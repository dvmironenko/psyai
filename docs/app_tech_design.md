# Технические требования веб-приложения

## Технологии

- **Python 3.11** – основной язык программирования.
- **FastAPI** – REST‑API, OAuth2PasswordBearer, Pydantic схемы.
- **Flask + Jinja2** – серверный рендеринг страниц, сессии, CSRF‑защита.
- **PostgreSQL** – реляционная БД (хост `db.mironenko.org`, пользователь `psyai_user`).
- **SQLAlchemy** – ORM, миграции через Alembic.
- **Passlib (bcrypt)** – хеширование паролей.
- **JWT** – токены доступа, срок 30 минут.
- **httpx** – HTTP‑клиент для взаимодействия Flask ↔ FastAPI.
- **pytest + httpx** – unit‑тесты эндпоинтов и моделей.
- **black, isort** – форматирование кода.
- **pre‑commit** – линтинг при коммите.

## Структура проекта

```sql
psyai_app/
├─ app/
│  ├─ api/              # FastAPI
│  │  ├─ main.py
│  │  └─ routers/
│  │     ├─ auth.py
│  │     ├─ users.py
│  │     ├─ admin.py
│  │     └─ sessions.py
│  ├─ models.py         # SQLAlchemy модели
│  ├─ schemas.py        # Pydantic схемы
│  ├─ database.py       # engine, SessionLocal
│  ├─ api.py            # Основной API роутер
│  └─ auth.py           # Аутентификационные функции
├─ flask_app/
│  ├─ main.py           # Flask + Jinja2
│  └─ templates/
│     ├─ index.html
│     ├─ login.html
│     ├─ register.html
│     ├─ dashboard.html
│     └─ admin.html
├─ alembic/             # миграции
├─ README.md
```

## Модели данных

### Модель User

- Используются таблицы: `users` и `users_plans`
- Модель SQLAlchemy `User` в `app/models.py`
- Поля: 
  - `is_active` (устанавливается в `false` для деактивации пользователя)

### Модель UserPlan

- Таблица `users_plans` в БД
- Определяет доступные планы доступа пользователей
- Поля: `id`, `name`, `description`

## Аутентификация

- Использовать OAuth2PasswordBearer, bcrypt для хеширования паролей
- Эндпоинты `/auth/login` (POST) и `/auth/register` (POST)
- JWT-токен хранить в cookie/сессии Flask
- Проверка пароля осуществляется с использованием `passlib` с алгоритмом bcrypt
- Пароли хешируются при регистрации и проверяются при входе
- Токены имеют срок действия 30 минут
- Валидация пароля: минимум 8 символов
- Восстановление пароля через `/api/auth/reset-password` (POST)
- Деактивация аккаунта через `/api/users/deactivate` (DELETE) для пользователей и `/api/admin/users/{user_id}/deactivate` (DELETE) для администраторов

## FastAPI маршруты

### Основные эндпоинты

- `/api/users/me` – текущий пользователь
- `/api/users/me/profile` – профиль текущего пользователя (GET) и обновление профиля (PUT/PATCH)
- `/api/auth/login` – вход пользователя (POST)
- `/api/auth/register` – регистрация пользователя (POST)
- `/api/auth/reset-password` – запрос на восстановление пароля (POST)

### Административные эндпоинты

- `/api/admin/users` – CRUD для пользователей (только роль `admin`)
- `/api/admin/plans` – CRUD для планов доступа (только роль `admin`)
- `/api/admin/stats` – статистика системы (только роль `admin`)
- `/api/admin/users/{user_id}/deactivate` – деактивация аккаунта пользователя (только роль `admin`)

### Системные эндпоинты

- `/api/health` – проверка состояния сервиса
- `/api/db_status` – статус подключения к БД
- `/api/users/deactivate` – деактивация собственного аккаунта (только авторизованный пользователь)

## Flask + Jinja2

### Публичные страницы

- Главная `/` – доступна всем
- Страница входа `/login`, регистрация `/register`

### Защищённые страницы

- Dashboard `/dashboard` – защищённый, рендерит `templates/dashboard.html`
- Админ-панель `/admin` – защищённый, рендерит `templates/admin.html`

### Системные страницы

- Logout `/logout` – завершение сеанса

## Интеграция

- Flask использует `httpx` для запросов к FastAPI, передавая JWT в заголовке `Authorization`
- Передача токена в заголовке: `Authorization: Bearer <token>`
- Все запросы к FastAPI API выполняются через переменную окружения `API_URL`
- Обработка ошибок API: перенаправление на страницу входа при недействительном токена
- Все HTTP-запросы включают обработку исключений и логирование

## Безопасность

- Хранить `SECRET_KEY` в переменных окружения
- В Flask включить `flask_session`
- FastAPI проверяет токен через `Depends(get_current_user)`
- Использование HTTPS в production окружении
- Защита от CSRF с помощью Flask-Session
- Ограничение времени действия JWT токенов (30 минут)
- Все пароли хешируются с использованием bcrypt
- Проверка и валидация входных данных на стороне сервера
- Защита от SQL-инъекций через использование SQLAlchemy ORM

## Тестирование и CI

- Unit-тесты для моделей и эндпоинтов (pytest + httpx)
- Linting (`black`, `isort`) через pre-commit

## Документация

- Swagger UI (`/docs`) генерируется автоматически FastAPI
- README с инструкциями по развёртыванию

## Развёртывание

- Переменные окружения: `DATABASE_URL`, `SECRET_KEY`, `API_URL` (base URL of the API service, e.g., `http://api:8000`)
- Переменная `FLASK_SECRET_KEY` для Flask приложения
- Все конфигурации хранятся в переменных окружения
- Используется alembic для миграций базы данных

## Важные замечания

- Не храните пароль `psyai_password` в репозитории – используйте переменные окружения
- Для JWT-токенов создайте `SECRET_KEY` (случайная строка)
- Убедитесь, что схема БД соответствует реальной базе