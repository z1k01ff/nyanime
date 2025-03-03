from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.dto.user import UserDto
from app.utils.custom_types import Int64

from .base import Base
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    """
    ORM-модель для представлення користувача Telegram бота в базі даних.
    
    Цей клас визначає структуру таблиці користувачів у базі даних
    та методи для роботи з даними користувача. Успадковує базовий клас
    SQLAlchemy та міксин для автоматичного відстеження часових міток.
    
    Attributes:
        __tablename__: Назва таблиці в базі даних.
        id: Унікальний ідентифікатор користувача в базі даних.
            Первинний ключ з автоінкрементом.
        telegram_id: Ідентифікатор користувача в Telegram.
                    Унікальне значення для пошуку користувача.
        name: Ім'я користувача для відображення.
        language: Обрана мова інтерфейсу (2-символьний код).
        language_code: Код мови користувача з Telegram.
                      Може бути None, якщо не визначено.
        blocked_at: Дата та час, коли користувач заблокував бота.
                   Може бути None, якщо користувач не блокував бота.
        
    Inherited Attributes (від TimestampMixin):
        created_at: Дата та час створення запису.
        updated_at: Дата та час останнього оновлення запису.
    """
    
    __tablename__ = "users"  # Назва таблиці в базі даних

    # Унікальний ідентифікатор користувача в базі даних
    id: Mapped[Int64] = mapped_column(primary_key=True, autoincrement=True)
    
    # Ідентифікатор користувача в Telegram (унікальний)
    telegram_id: Mapped[Int64] = mapped_column(unique=True)
    
    # Ім'я користувача для відображення
    name: Mapped[str] = mapped_column()
    
    # Обрана мова інтерфейсу (2-символьний код)
    language: Mapped[str] = mapped_column(String(length=2))
    
    # Код мови користувача з Telegram (може бути None)
    language_code: Mapped[Optional[str]] = mapped_column()
    
    # Дата та час, коли користувач заблокував бота (може бути None)
    blocked_at: Mapped[Optional[datetime]] = mapped_column()

    def dto(self) -> UserDto:
        """
        Перетворює ORM-модель користувача в об'єкт передачі даних (DTO).
        
        Цей метод створює об'єкт UserDto на основі поточного екземпляра
        моделі User, що дозволяє безпечно передавати дані користувача
        між різними частинами додатку без прив'язки до ORM.
        
        Returns:
            UserDto: Об'єкт передачі даних, що містить інформацію про користувача.
                    Включає додаткове поле bot_blocked, яке визначається на основі
                    наявності значення в полі blocked_at.
        """
        return UserDto.model_validate(self)
