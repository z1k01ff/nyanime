"""
Модуль для створення ключів зберігання даних.

Цей модуль містить базовий клас для створення структурованих ключів,
які використовуються для зберігання та отримання даних з кешу або бази даних.
"""

from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Optional
from uuid import UUID

from pydantic import BaseModel


class StorageKey(BaseModel):
    """
    Базовий клас для створення ключів зберігання даних.
    
    Цей клас дозволяє створювати структуровані ключі для зберігання даних,
    з підтримкою префіксів та розділювачів. Ключі формуються на основі
    полів моделі та можуть бути серіалізовані в рядок.
    
    Attributes:
        __separator__: Символ-розділювач для частин ключа (за замовчуванням ":")
        __prefix__: Необов'язковий префікс для всіх ключів цього типу
    """
    
    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        """Символ-розділювач даних (за замовчуванням :code:`:`)"""
        __prefix__: ClassVar[Optional[str]]
        """Префікс ключа зберігання"""

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Ініціалізує підклас StorageKey з вказаними параметрами.
        
        Встановлює розділювач та префікс для підкласу та перевіряє,
        що розділювач не міститься в префіксі.
        
        Args:
            **kwargs: Параметри для налаштування підкласу
                separator: Символ-розділювач (за замовчуванням ":")
                prefix: Префікс для ключів (за замовчуванням None)
                
        Raises:
            ValueError: Якщо розділювач міститься в префіксі
        """
        cls.__separator__ = kwargs.pop("separator", ":")
        cls.__prefix__ = kwargs.pop("prefix", None)
        if cls.__separator__ in (cls.__prefix__ or ""):
            raise ValueError(
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
        super().__init_subclass__(**kwargs)

    @classmethod
    def encode_value(cls, value: Any) -> str:
        """
        Кодує значення в рядок для використання в ключі.
        
        Перетворює різні типи даних (None, Enum, UUID, bool) на рядкове представлення.
        
        Args:
            value: Значення для кодування
            
        Returns:
            str: Рядкове представлення значення
        """
        if value is None:
            return "null"
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        return str(value)

    def pack(self) -> str:
        """
        Упаковує всі поля моделі в єдиний рядок-ключ.
        
        Формує ключ, об'єднуючи префікс та закодовані значення полів
        за допомогою розділювача.
        
        Returns:
            str: Повний ключ для зберігання
            
        Raises:
            ValueError: Якщо будь-яке значення містить символ-розділювач
        """
        result = [self.__prefix__] if self.__prefix__ else []
        for key, value in self.model_dump(mode="json").items():
            encoded = self.encode_value(value)
            if self.__separator__ in encoded:
                raise ValueError(
                    f"Separator symbol {self.__separator__!r} can not be used "
                    f"in value {key}={encoded!r}"
                )
            result.append(encoded)
        return self.__separator__.join(result)
