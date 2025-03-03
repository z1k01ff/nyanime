"""
Модуль для обробки подій, пов'язаних зі статусом бота в приватних чатах.

Цей модуль відстежує блокування та розблокування бота користувачами
і оновлює відповідну інформацію в базі даних.
"""

from __future__ import annotations

from typing import Any, Final

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from app.models.dto.user import UserDto
from app.services.user import UserService
from app.utils.time import datetime_now

# Створення маршрутизатора для обробників подій в приватних чатах
router: Final[Router] = Router(name=__name__)
# Фільтрація подій тільки для приватних чатів
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_unblocked(_: ChatMemberUpdated, user: UserDto, user_service: UserService) -> Any:
    """
    Обробник події розблокування бота користувачем.
    
    Оновлює статус користувача в базі даних, встановлюючи blocked_at як None.
    
    Args:
        _: Об'єкт події оновлення статусу учасника чату (не використовується)
        user: Дані користувача, який розблокував бота
        user_service: Сервіс для роботи з даними користувачів
        
    Returns:
        None
    """
    await user_service.update(user=user, blocked_at=None)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def bot_blocked(_: ChatMemberUpdated, user: UserDto, user_service: UserService) -> Any:
    """
    Обробник події блокування бота користувачем.
    
    Оновлює статус користувача в базі даних, встановлюючи поточний час як blocked_at.
    
    Args:
        _: Об'єкт події оновлення статусу учасника чату (не використовується)
        user: Дані користувача, який заблокував бота
        user_service: Сервіс для роботи з даними користувачів
        
    Returns:
        None
    """
    await user_service.update(user=user, blocked_at=datetime_now())
