from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.models.config import AppConfig


def create_session_pool(config: AppConfig) -> async_sessionmaker[AsyncSession]:
    """
    Створює та повертає пул асинхронних сесій SQLAlchemy.
    
    Функція ініціалізує асинхронний двигун SQLAlchemy з параметрами з конфігурації
    та створює фабрику сесій для роботи з базою даних.
    
    Args:
        config: Об'єкт конфігурації додатку, що містить налаштування для PostgreSQL та SQLAlchemy
        
    Returns:
        Фабрика асинхронних сесій SQLAlchemy, яка використовується для створення
        нових сесій для взаємодії з базою даних
    """
    # Створюємо асинхронний двигун SQLAlchemy з параметрами з конфігурації
    engine: AsyncEngine = create_async_engine(
        # URL для підключення до PostgreSQL
        url=config.postgres.build_url(),
        # Налаштування логування SQL-запитів
        echo=config.sql_alchemy.echo,
        echo_pool=config.sql_alchemy.echo_pool,
        # Налаштування пулу з'єднань
        pool_size=config.sql_alchemy.pool_size,
        max_overflow=config.sql_alchemy.max_overflow,
        pool_timeout=config.sql_alchemy.pool_timeout,
        pool_recycle=config.sql_alchemy.pool_recycle,
    )
    
    # Створюємо та повертаємо фабрику асинхронних сесій
    # expire_on_commit=False запобігає автоматичному оновленню об'єктів після commit
    return async_sessionmaker(engine, expire_on_commit=False)
