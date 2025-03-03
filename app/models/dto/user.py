from datetime import datetime
from typing import Optional

from aiogram import html
from aiogram.utils.link import create_tg_link

from app.models.base import PydanticModel


class UserDto(PydanticModel):
    """
    Об'єкт передачі даних (DTO) для користувача Telegram бота.
    
    Цей клас представляє користувача в системі та містить всю необхідну
    інформацію про нього, включаючи ідентифікатори, ім'я, мову та статус.
    Успадковує базову модель Pydantic для валідації та серіалізації.
    
    Attributes:
        id: Внутрішній ідентифікатор користувача в базі даних.
        telegram_id: Ідентифікатор користувача в Telegram.
        name: Ім'я користувача для відображення.
        language: Обрана мова інтерфейсу.
        language_code: Код мови користувача з Telegram.
                      Може бути None, якщо не визначено.
        bot_blocked: Прапорець, що вказує, чи заблокував користувач бота.
                    За замовчуванням: False.
        blocked_at: Дата та час, коли користувач заблокував бота.
                   Може бути None, якщо користувач не блокував бота.
    """
    
    id: int  # Внутрішній ідентифікатор в базі даних
    telegram_id: int  # Ідентифікатор користувача в Telegram
    name: str  # Ім'я користувача для відображення
    language: str  # Обрана мова інтерфейсу
    language_code: Optional[str] = None  # Код мови користувача з Telegram
    bot_blocked: bool = False  # Чи заблокував користувач бота
    blocked_at: Optional[datetime] = None  # Дата та час блокування бота

    @property
    def url(self) -> str:
        """
        Створює URL-посилання на профіль користувача в Telegram.
        
        Returns:
            str: URL-посилання на профіль користувача у форматі
                 "tg://user?id={telegram_id}"
        """
        return create_tg_link("user", id=self.telegram_id)

    @property
    def mention(self) -> str:
        """
        Створює HTML-посилання на користувача з його іменем.
        
        Це посилання можна використовувати в повідомленнях Telegram
        для згадування користувача з можливістю переходу на його профіль.
        
        Returns:
            str: HTML-посилання на користувача у форматі
                 "<a href='tg://user?id={telegram_id}'>{name}</a>"
        """
        return html.link(value=self.name, link=self.url)
