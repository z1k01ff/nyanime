from __future__ import annotations

from app.models.config.env import (
    AppConfig,
    CommonConfig,
    PostgresConfig,
    RedisConfig,
    ServerConfig,
    SQLAlchemyConfig,
    TelegramConfig,
)


# noinspection PyArgumentList
def create_app_config() -> AppConfig:
    """
    Створює та повертає конфігурацію додатку.
    
    Функція ініціалізує всі необхідні конфігураційні об'єкти для роботи додатку,
    включаючи налаштування для Telegram, PostgreSQL, SQLAlchemy, Redis та сервера.
    Конфігурація завантажується з змінних середовища за допомогою Pydantic.
    
    Returns:
        Об'єкт AppConfig з усіма налаштуваннями додатку
    """
    return AppConfig(
        # Конфігурація для роботи з Telegram API
        telegram=TelegramConfig(),
        
        # Конфігурація для підключення до PostgreSQL
        postgres=PostgresConfig(),
        
        # Конфігурація для роботи з SQLAlchemy ORM
        sql_alchemy=SQLAlchemyConfig(),
        
        # Конфігурація для підключення до Redis
        redis=RedisConfig(),
        
        # Конфігурація веб-сервера для режиму webhook
        server=ServerConfig(),
        
        # Загальні налаштування додатку
        common=CommonConfig(),
    )
