"""
Модуль, що містить проміжний обробник для роботи з користувачами.

Цей модуль відповідає за отримання або створення користувачів у базі даних
на основі даних, отриманих від Telegram API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram.types import TelegramObject
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nMiddleware

from app.services.user import UserService
from app.telegram.middlewares.event_typed import EventTypedMiddleware
from app.utils.logging import database as logger

if TYPE_CHECKING:
    from app.models.dto.user import UserDto


class UserMiddleware(EventTypedMiddleware):
    """
    Проміжний обробник для роботи з користувачами.
    
    Цей клас відповідає за:
    1. Отримання даних користувача з бази даних за його Telegram ID
    2. Створення нового користувача, якщо він не існує в базі даних
    3. Додавання об'єкта користувача до контексту обробника
    
    Наслідує EventTypedMiddleware для автоматичної реєстрації на відповідні типи подій.
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        """
        Обробляє подію та додає дані користувача до контексту.
        
        Args:
            handler: Наступний обробник у ланцюжку
            event: Об'єкт події Telegram
            data: Словник з даними контексту
            
        Returns:
            Результат виконання наступного обробника
        """
        # Отримання об'єкта користувача Telegram з даних події
        aiogram_user: Optional[AiogramUser] = data.get("event_from_user")
        if aiogram_user is None or aiogram_user.is_bot:
            # Пропускаємо ботів та події без користувача
            # Запобігає додаванню самого бота до бази даних
            # при прийнятті запитів на приєднання до чату та отриманні оновлень про учасників чату
            return await handler(event, data)

        # Створення сервісу для роботи з користувачами та додавання його до контексту
        user_service = data["user_service"] = UserService(
            session_pool=data["session_pool"],
            redis=data["redis"],
            config=data["config"],
        )

        # Спроба отримати користувача з бази даних за його Telegram ID
        user: Optional[UserDto] = await user_service.by_tg_id(telegram_id=aiogram_user.id)
        if user is None:
            # Якщо користувач не знайдений, створюємо нового
            i18n: I18nMiddleware = data["i18n_middleware"]
            user = await user_service.create(aiogram_user=aiogram_user, i18n_core=i18n.core)
            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        # Додаємо об'єкт користувача до контексту для використання в обробниках
        data["user"] = user
        return await handler(event, data)
