from typing import Any, Optional

from app.models.sql import User

from .base import BaseRepository


class UsersRepository(BaseRepository):
    """
    Репозиторій для роботи з користувачами в базі даних.
    
    Цей клас надає методи для виконання CRUD операцій (створення, читання, 
    оновлення, видалення) над моделлю User. Він наслідується від BaseRepository,
    який містить базову функціональність для роботи з базою даних.
    """

    async def get(self, user_id: int) -> Optional[User]:
        """
        Отримує користувача за його ID.
        
        Args:
            user_id: Унікальний ідентифікатор користувача
            
        Returns:
            User: Об'єкт користувача, якщо знайдено
            None: Якщо користувача з таким ID не існує
        """
        # Використовуємо базовий метод _get для отримання користувача за ID
        return await self._get(User, User.id == user_id)

    async def by_tg_id(self, telegram_id: int) -> Optional[User]:
        """
        Отримує користувача за його Telegram ID.
        
        Args:
            telegram_id: ID користувача в Telegram
            
        Returns:
            User: Об'єкт користувача, якщо знайдено
            None: Якщо користувача з таким Telegram ID не існує
        """
        # Шукаємо користувача за його Telegram ID замість звичайного ID
        return await self._get(User, User.telegram_id == telegram_id)

    async def update(self, user_id: int, **kwargs: Any) -> Optional[User]:
        """
        Оновлює дані користувача.
        
        Args:
            user_id: Унікальний ідентифікатор користувача
            **kwargs: Поля та їх нові значення для оновлення
            
        Returns:
            User: Оновлений об'єкт користувача, якщо load_result=True
            None: Якщо користувача не знайдено або load_result=False
            
        Приклад:
            await users_repo.update(user_id=123, name="Нове ім'я", age=30)
        """
        # Оновлюємо користувача, використовуючи базовий метод _update
        # model - модель даних (User)
        # conditions - умови для пошуку (id == user_id)
        # load_result=False - не повертати оновлений об'єкт
        # **kwargs - поля для оновлення (name="Нове ім'я", тощо)
        return await self._update(
            model=User,
            conditions=[User.id == user_id],
            load_result=False,
            **kwargs,
        )

    async def delete(self, user_id: int) -> bool:
        """
        Видаляє користувача з бази даних.
        
        Args:
            user_id: Унікальний ідентифікатор користувача
            
        Returns:
            bool: True, якщо користувача успішно видалено, False - якщо користувача не знайдено
        """
        # Видаляємо користувача за його ID
        # Повертає True, якщо видалення успішне, False - якщо користувача не знайдено
        return await self._delete(User, User.id == user_id)
