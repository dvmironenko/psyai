# PsyAI - Кабинет психолога

Веб-приложение для кабинета психолога с интеграцией FastAPI (REST API) и Flask (серверный рендеринг).

## Структура проекта

```
psyai/
├── app/                 # FastAPI приложение
│   ├── main.py          # Главная точка входа
│   ├── config.py        # Конфигурация
│   ├── database.py      # Подключение к БД
│   ├── models.py        # Модели SQLAlchemy
│   ├── schemas.py       # Pydantic схемы
│   ├── auth.py          # Аутентификация (JWT)
│   └── routers/         # API роутеры
│       ├── auth.py      # /auth/*
│       ├── users.py     # /users/*
│       └── admin.py     # /admin/*
├── flask_app/           # Flask приложение
│   ├── main.py          # Главная точка входа
│   └── templates/       # HTML шаблоны
├── alembic/             # Миграции базы данных
└── tests/               # Unit-тесты
```

## Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd psyai

# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## Переменные окружения

```bash
# База данных
DATABASE_URL=postgresql://user:password@host/database

# Ключи шифрования
SECRET_KEY=your-secret-key-change-in-production
FLASK_SECRET_KEY=your-flask-secret-key

# URL FastAPI сервиса (для Flask интеграции)
API_URL=http://localhost:8000

# Окружение
ENVIRONMENT=development  # или production
```

## Запуск

### Миграции базы данных

```bash
alembic upgrade head
```

### Запуск FastAPI (API)

```bash
uvicorn app.main:app --reload --port 8000
```

FastAPI будет доступен по адресу: `http://localhost:8000`
Документация Swagger UI: `http://localhost:8000/docs`

### Запуск Flask (frontend)

```bash
flask --app flask_app/main.py run --debug
```

Flask будет доступен по адресу: `http://localhost:5000`

## Команды разработки

```bash
# Форматирование кода
black .
isort .

# Линтинг (с pre-commit)
pre-commit run --all-files

# Запуск тестов
pytest

# Покрытие тестами
pytest --cov=app --cov-report=html
```

## API эндпоинты

### Auth
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход (возвращает JWT токен)
- `POST /api/v1/auth/reset-password` - Восстановление пароля

### Users
- `GET /api/v1/users/me` - Текущий пользователь
- `PUT /api/v1/users/me/profile` - Обновление профиля
- `DELETE /api/v1/users/deactivate` - Деактивация аккаунта

### Admin
- `GET /api/v1/admin/users` - Список пользователей
- `CRUD /api/v1/admin/users/{id}` - Управление пользователем
- `CRUD /api/v1/admin/plans` - Управление планами
- `GET /api/v1/admin/stats` - Статистика

## Планы доступа

| ID | Название | Описание |
|----|----------|----------|
| 0 | Free | Бесплатный план |
| 1 | Basic | Базовый план |
| 2 | Premium | Премиум план |
| 3 | Ultra | Ультра план |
