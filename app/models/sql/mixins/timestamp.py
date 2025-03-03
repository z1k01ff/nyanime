from datetime import datetime
from typing import Any, Final

from sqlalchemy import Function, func
from sqlalchemy.orm import Mapped, mapped_column

# Функція для отримання поточного часу в UTC
# Використовується як значення за замовчуванням для полів created_at та updated_at
NowFunc: Final[Function[Any]] = func.timezone("UTC", func.now())


class TimestampMixin:
    """
    Міксин для додавання полів часових міток до моделей SQLAlchemy.
    
    Цей клас додає до моделей SQLAlchemy поля created_at та updated_at,
    які автоматично заповнюються при створенні та оновленні записів.
    Використовується для відстеження часу створення та останньої зміни
    записів у базі даних.
    
    Attributes:
        created_at: Дата та час створення запису. Автоматично заповнюється
                   поточним часом у UTC при створенні запису.
        updated_at: Дата та час останнього оновлення запису. Автоматично
                   заповнюється поточним часом у UTC при створенні та
                   оновленні запису.
    """
    
    # Дата та час створення запису
    # Автоматично заповнюється поточним часом у UTC при створенні запису
    created_at: Mapped[datetime] = mapped_column(server_default=NowFunc)
    
    # Дата та час останнього оновлення запису
    # Автоматично заповнюється поточним часом у UTC при створенні та оновленні запису
    updated_at: Mapped[datetime] = mapped_column(server_default=NowFunc, server_onupdate=NowFunc)
