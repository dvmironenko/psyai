# Пошаговый план разработки приложения

## Контекст
- Проект – **Python/Flask** API, без отдельного клиентского фронтенда.
- В репозитории пока нет конкретной структуры (`app.py`, `models.py` и т.п.) – планируем стандартную организацию.
- Требуется: REST‑API с аутентификацией, CRUD‑операции над сущностями (например, `User`, `Post`), базовая документацию и тесты.

## Цели
1. Создать рабочий Flask‑сервер, подключённый к базе данных PostgreSQL.
2. Реализовать эндпоинты для пользователей и постов (создание, чтение, обновление, удаление).
3. Добавить JWT‑аутентификацию и защиту эндпоинтов.
4. Обеспечить покрытие unit‑тестами (pytest) и интеграционными тестами.
5. Подготовить Docker‑образ для развертывания.

## Структура проекта (предлагаемая)
```
project/
├── app.py                 # Flask‑приложение и конфигурация
├── config.py              # Конфиги (dev, prod)
├── models/
│   ├── __init__.py
│   └── user.py            # Модель User (SQLAlchemy)
├── routes/
│   ├── __init__.py
│   └── auth.py            # Регистрация, login, logout
├── services/
│   └── user_service.py   # бизнес‑логика
├── tests/
│   ├── conftest.py        # фикстуры для тестов
│   └── test_auth.py
├── requirements.txt
└── Dockerfile
```

## Шаги реализации
1. **Инициализация проекта**
   - Создать виртуальное окружение (`python3 -m venv .venv`).
   - Установить зависимости: `Flask`, `SQLAlchemy`, `psycopg2-binary`, `PyJWT`, `pytest`.
   - Создать базовый файл `app.py` с фабрикой приложения.
2. **Конфигурация**
   - `config.py` с классами `DevelopmentConfig`, `ProductionConfig`.
   - Переменные окружения для DB‑URL, SECRET_KEY и JWT_SECRET.
3. **Модели**
   - Определить `User` (id, email, password_hash, created_at).
   - Добавить миграции с `Flask-Migrate` (если понадобится).
4. **Аутентификация**
   - `routes/auth.py`: `/register`, `/login` – возвращают JWT.
   - Хешировать пароли с `werkzeug.security.generate_password_hash`.
5. **Защита эндпоинтов**
   - Декоратор `@jwt_required` для защищённых маршрутов.
6. **CRUD‑эндпоинты**
   - `routes/posts.py`: `/posts` (GET, POST), `/posts/<id>` (PUT, DELETE).
   - Использовать сервисы для бизнес‑логики.
7. **Тесты**
   - `tests/conftest.py`: фикстура Flask‑теста.
   - Написать unit‑тесты для `auth` и `posts` (запросы через `client`).
8. **Документация**
   - Добавить OpenAPI/Swagger через `flasgger` или `apispec`.
9. **Docker**
   - *Removed: Docker setup.*
10. **CI/CD** (опционально)
    - GitHub Actions: lint, test, build Docker image.

## Проверка/верификация
- Запустить `pytest` – все тесты должны проходить.
- Сгенерировать и открыть Swagger UI, проверить эндпоинты вручную.
- Поднять контейнеры `docker-compose up --build` и убедиться, что сервис доступен.
- Проверить JWT‑аутентификацию: регистрация → login → protected request.

## Зависимости и файлы, которые будут созданы/изменены
- `app.py`, `config.py`
- каталог `models` (создать `__init__.py`, `user.py`)
- каталог `routes` (`__init__.py`, `auth.py`, `posts.py`)
- каталог `services` (`user_service.py`)
- `requirements.txt`
- `Dockerfile`, `docker-compose.yml`
- каталог `tests` (создать структуру)
