"""Основной модуль Flask приложения."""

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session as FlaskSession
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import httpx

# Импорт из FastAPI приложения
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import config


def create_app():
    """Фабрика Flask приложения."""
    app = Flask(__name__)

    # Конфигурация
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["API_URL"] = config.API_URL

    FlaskSession(app)

    # API client
    api_client = httpx.Client(
        base_url=config.API_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    @app.context_processor
    def inject_api_url():
        return {"api_url": config.API_URL}

    @app.route("/")
    def index():
        """Главная страница."""
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """Страница входа."""
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            try:
                # Запрос к FastAPI
                response = api_client.post(
                    "/auth/login",
                    data={"username": email, "password": password}
                )
                response.raise_for_status()

                token_data = response.json()
                session["access_token"] = token_data["access_token"]
                return redirect(url_for("dashboard"))

            except httpx.HTTPStatusError:
                error = "Неверный email или пароль"
            except httpx.RequestError:
                error = "Ошибка подключения к серверу"

            return render_template("login.html", error=error)

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        """Страница регистрации."""
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            try:
                response = api_client.post(
                    "/auth/register",
                    data={"email": email, "password": password}
                )
                response.raise_for_status()

                return redirect(url_for("login"))

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 400:
                    error = "Этот email уже зарегистрирован"
                else:
                    error = "Ошибка регистрации"
            except httpx.RequestError:
                error = "Ошибка подключения к серверу"

            return render_template("register.html", error=error)

        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard():
        """Защищённый dashboard."""
        access_token = session.get("access_token")
        if not access_token:
            return redirect(url_for("login"))

        try:
            response = api_client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            user = response.json()

            return render_template("dashboard.html", user=user)

        except httpx.HTTPStatusError:
            session.pop("access_token", None)
            return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        """Выход."""
        session.pop("access_token", None)
        return redirect(url_for("index"))

    @app.route("/admin")
    def admin():
        """Админ-панель."""
        access_token = session.get("access_token")
        if not access_token:
            return redirect(url_for("login"))

        try:
            response = api_client.get(
                "/admin/stats",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            stats = response.json()

            return render_template("admin.html", stats=stats)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                return "Доступ запрещён", 403
            session.pop("access_token", None)
            return redirect(url_for("login"))

    return app


# Создание приложения для wsgi
app = create_app()
