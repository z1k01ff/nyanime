from typing import Any, Awaitable, Callable, Optional, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.cores import BaseCore
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.config import AppConfig
from app.models.dto.user import UserDto
from app.models.sql import User
from app.services.database import RedisRepository, SQLSessionContext


class UserService:
    """
    Сервіс для роботи з користувачами.
    
    Забезпечує створення, отримання та оновлення користувачів з використанням
    SQL бази даних та Redis кешування.
    """
    session_pool: async_sessionmaker[AsyncSession]
    redis: RedisRepository
    config: AppConfig

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession],
        redis: RedisRepository,
        config: AppConfig,
    ) -> None:
        """
        Ініціалізує сервіс користувача.
        
        Args:
            session_pool: Пул асинхронних сесій SQLAlchemy
            redis: Репозиторій для роботи з Redis
            config: Конфігурація додатку
        """
        self.session_pool = session_pool
        self.redis = redis
        self.config = config

    async def create(
        self,
        aiogram_user: AiogramUser,
        i18n_core: BaseCore[Any],
    ) -> UserDto:
        """
        Створює нового користувача на основі даних з Telegram.
        
        Args:
            aiogram_user: Об'єкт користувача Aiogram
            i18n_core: Ядро інтернаціоналізації для визначення мови
            
        Returns:
            DTO об'єкт створеного користувача
        """
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            user: User = User(
                telegram_id=aiogram_user.id,
                name=aiogram_user.full_name,
                language=(
                    # Використовуємо мову користувача, якщо вона підтримується,
                    # інакше використовуємо мову за замовчуванням
                    aiogram_user.language_code
                    if aiogram_user.language_code in i18n_core.locales
                    else cast(str, i18n_core.default_locale)
                ),
                language_code=aiogram_user.language_code,
            )
            await uow.commit(user)
        return user.dto()

    async def _get(
        self,
        getter: Callable[[Any], Awaitable[Optional[User]]],
        key: Any,
    ) -> Optional[UserDto]:
        """
        Внутрішній метод для отримання користувача з кешу або бази даних.
        
        Спочатку перевіряє наявність користувача в Redis, якщо не знайдено,
        шукає в базі даних і кешує результат.
        
        Args:
            getter: Функція для отримання користувача з бази даних
            key: Ключ для пошуку користувача
            
        Returns:
            DTO об'єкт користувача або None, якщо користувача не знайдено
        """
        # Спроба отримати користувача з Redis
        user_dto: Optional[UserDto] = await self.redis.get_user(key=key)
        if user_dto is not None:
            return user_dto
            
        # Якщо користувача немає в кеші, шукаємо в базі даних
        user: Optional[User] = await getter(key)
        if user is None:
            return None
            
        # Зберігаємо користувача в Redis для майбутніх запитів
        await self.redis.save_user(
            key=user.telegram_id,
            value=(user_dto := user.dto()),
            cache_time=self.config.common.users_cache_time,
        )
        return user_dto

    async def get(self, user_id: int) -> Optional[UserDto]:
        """
        Отримує користувача за його ID.
        
        Args:
            user_id: ID користувача в базі даних
            
        Returns:
            DTO об'єкт користувача або None, якщо користувача не знайдено
        """
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            return await self._get(repository.users.get, user_id)

    async def by_tg_id(self, telegram_id: int) -> Optional[UserDto]:
        """
        Отримує користувача за його Telegram ID.
        
        Args:
            telegram_id: ID користувача в Telegram
            
        Returns:
            DTO об'єкт користувача або None, якщо користувача не знайдено
        """
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            return await self._get(repository.users.by_tg_id, telegram_id)

    async def update(self, user: UserDto, **kwargs: Any) -> None:
        """
        Оновлює дані користувача.
        
        Оновлює атрибути користувача в базі даних та в кеші Redis.
        
        Args:
            user: DTO об'єкт користувача для оновлення
            kwargs: Пари ключ-значення для оновлення атрибутів користувача
        """
        # Оновлюємо атрибути користувача
        for key, value in kwargs.items():
            setattr(user, key, value)
            
        # Оновлюємо користувача в базі даних
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            await repository.users.update(user_id=user.id, **user.model_state)
            
        # Оновлюємо користувача в Redis
        await self.redis.save_user(
            key=user.telegram_id,
            value=user,
            cache_time=self.config.common.users_cache_time,
        )
