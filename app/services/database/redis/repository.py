from __future__ import annotations

from typing import Any, Optional, TypeVar

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.models.dto.user import UserDto
from app.utils import mjson
from app.utils.key_builder import StorageKey

from .keys import UserKey

# Типовий параметр для валідації даних
T = TypeVar("T", bound=Any)


class RedisRepository:
    """
    Репозиторій для роботи з Redis.
    
    Надає методи для збереження, отримання та видалення даних у Redis,
    включаючи спеціалізовані методи для роботи з користувачами.
    """
    
    def __init__(self, client: Redis) -> None:
        """
        Ініціалізує репозиторій з клієнтом Redis.
        
        Args:
            client: Асинхронний клієнт Redis для виконання операцій
        """
        self.client = client

    async def get(self, key: StorageKey, validator: type[T]) -> Optional[T]:
        """
        Отримує дані з Redis та валідує їх за допомогою вказаного типу.
        
        Args:
            key: Ключ для пошуку даних у Redis
            validator: Тип для валідації отриманих даних
            
        Returns:
            Валідований об'єкт або None, якщо дані не знайдено
        """
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return None
        # Декодуємо JSON-дані
        value = mjson.decode(value)
        # Валідуємо дані за допомогою TypeAdapter
        return TypeAdapter[T](validator).validate_python(value)

    async def set(self, key: StorageKey, value: Any, ex: Optional[ExpiryT] = None) -> None:
        """
        Зберігає дані в Redis.
        
        Args:
            key: Ключ для збереження даних
            value: Дані для збереження (можуть бути Pydantic моделлю)
            ex: Час життя запису (в секундах або як Redis ExpiryT)
        """
        # Якщо значення є Pydantic моделлю, конвертуємо її в словник
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        # Зберігаємо закодовані дані в Redis
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def delete(self, key: StorageKey) -> None:
        """
        Видаляє дані з Redis за вказаним ключем.
        
        Args:
            key: Ключ для видалення даних
        """
        await self.client.delete(key.pack())

    async def close(self) -> None:
        """
        Закриває з'єднання з Redis.
        """
        await self.client.aclose(close_connection_pool=True)

    async def save_user(self, key: Any, value: UserDto, cache_time: int) -> None:
        """
        Зберігає дані користувача в Redis.
        
        Args:
            key: Ідентифікатор користувача
            value: DTO об'єкт користувача для збереження
            cache_time: Час життя запису в секундах
        """
        user_key: UserKey = UserKey(key=key)
        await self.set(key=user_key, value=value, ex=cache_time)

    async def get_user(self, key: Any) -> Optional[UserDto]:
        """
        Отримує дані користувача з Redis.
        
        Args:
            key: Ідентифікатор користувача
            
        Returns:
            DTO об'єкт користувача або None, якщо користувача не знайдено
        """
        user_key: UserKey = UserKey(key=key)
        return await self.get(key=user_key, validator=UserDto)

    async def delete_user(self, key: Any) -> None:
        """
        Видаляє дані користувача з Redis.
        
        Args:
            key: Ідентифікатор користувача
        """
        user_key: UserKey = UserKey(key=key)
        await self.delete(user_key)
