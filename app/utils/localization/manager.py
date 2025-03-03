"""
Модуль для управління локалізацією та мовними налаштуваннями користувачів.

Цей модуль містить класи для отримання та встановлення мовних налаштувань
користувачів бота на основі їх профілю або налаштувань Telegram.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.managers import BaseManager

if TYPE_CHECKING:
    from app.models.dto.user import UserDto


class UserManager(BaseManager):
    """
    Менеджер для управління мовними налаштуваннями користувачів.
    
    Цей клас відповідає за отримання та встановлення мовних налаштувань
    користувачів на основі їх профілю в базі даних або налаштувань Telegram.
    
    Наслідує BaseManager з aiogram_i18n для інтеграції з системою локалізації.
    """
    
    async def get_locale(
        self,
        event_from_user: Optional[AiogramUser] = None,
        user: Optional[UserDto] = None,
    ) -> str:
        """
        Отримує мовний код для користувача.
        
        Пріоритет визначення мови:
        1. Мова з профілю користувача в базі даних (якщо доступна)
        2. Мова з налаштувань Telegram користувача (якщо доступна)
        3. Мова за замовчуванням з конфігурації бота
        
        Args:
            event_from_user: Об'єкт користувача Telegram з події
            user: Об'єкт користувача з бази даних
            
        Returns:
            str: Код мови для використання в повідомленнях
        """
        locale: Optional[str] = None
        if user is not None:
            # Спочатку перевіряємо мову з профілю користувача
            locale = user.language
        elif event_from_user is not None and event_from_user.language_code is not None:
            # Якщо профіль недоступний, використовуємо мову з Telegram
            locale = event_from_user.language_code
        # Повертаємо знайдену мову або мову за замовчуванням
        return locale or cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: UserDto) -> None:
        """
        Встановлює мовний код для користувача.
        
        Цей метод повинен оновлювати мовні налаштування користувача в базі даних.
        
        Args:
            locale: Код мови для встановлення
            user: Об'єкт користувача, для якого встановлюється мова
            
        Raises:
            NotImplementedError: Метод не реалізований і повинен бути перевизначений
        """
        raise NotImplementedError()
