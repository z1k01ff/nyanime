"""
Модуль для обробки помилок, які виникають під час роботи Telegram бота.

Цей модуль містить обробники для різних типів винятків, що можуть виникнути
під час обробки повідомлень та запитів користувачів.
"""

from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

from app.exceptions.base import BotError

# Створення маршрутизатора для обробників помилок
router: Final[Router] = Router(name=__name__)


@router.error(ExceptionTypeFilter(BotError), F.update.message)
async def handle_some_error(error: ErrorEvent, i18n: I18nContext) -> Any:
    """
    Обробник для помилок типу BotError, які виникають при обробці повідомлень.
    
    Відправляє користувачу повідомлення про те, що щось пішло не так.
    
    Args:
        error: Об'єкт події помилки, що містить інформацію про виняток
        i18n: Контекст інтернаціоналізації для перекладів
        
    Returns:
        Відповідь користувачу з повідомленням про помилку
    """
    await error.update.message.answer(text=i18n.messages.something_went_wrong(_path="errors.ftl"))
