"""
Модуль для обробки основних команд меню Telegram бота.

Цей модуль містить обробники для стартової команди та взаємодії з основним меню бота.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router, flags
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from app.telegram.keyboards.callback_data.menu import CDPing
from app.telegram.keyboards.menu import ping_keyboard

if TYPE_CHECKING:
    from app.models.dto.user import UserDto

# Створення маршрутизатора для обробників меню
router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def greeting(message: Message, i18n: I18nContext, user: UserDto) -> Any:
    """
    Обробник стартової команди (/start).
    
    Відправляє привітальне повідомлення користувачу та показує основне меню.
    
    Args:
        message: Об'єкт повідомлення від користувача
        i18n: Контекст інтернаціоналізації для перекладів
        user: Дані користувача, який відправив команду
        
    Returns:
        Відповідь з привітальним повідомленням та клавіатурою
    """
    return message.answer(
        text=i18n.messages.hello(name=user.mention, _path="menu.ftl"),
        reply_markup=ping_keyboard(i18n=i18n),
    )


@router.callback_query(CDPing.filter())
@flags.callback_answer(disabled=True)
async def answer_pong(query: CallbackQuery, i18n: I18nContext) -> Any:
    """
    Обробник натискання на кнопку "ping".
    
    Відповідає користувачу текстом "pong" без зміни повідомлення.
    
    Args:
        query: Об'єкт callback-запиту від натискання кнопки
        i18n: Контекст інтернаціоналізації для перекладів
        
    Returns:
        Відповідь на callback-запит з текстом "pong"
    """
    return query.answer(text=i18n.messages.pong(_path="menu.ftl"))
