"""
Модуль для роботи з JSON-серіалізацією та десеріалізацією.

Цей модуль надає функції для кодування та декодування об'єктів у форматі JSON
з використанням бібліотеки msgspec для високопродуктивної обробки.
"""

from typing import Any, Callable, Final

from msgspec.json import Decoder, Encoder

# Функція для декодування JSON-рядків у словники Python
decode: Final[Callable[..., Any]] = Decoder[dict[str, Any]]().decode

# Функція для кодування об'єктів Python у байтові JSON-представлення
bytes_encode: Final[Callable[..., bytes]] = Encoder().encode


def encode(obj: Any) -> str:
    """
    Кодує об'єкт Python у JSON-рядок.
    
    Ця функція перетворює об'єкт Python на JSON-рядок, використовуючи
    високопродуктивний кодувальник msgspec.
    
    Args:
        obj: Об'єкт Python для кодування (словник, список, рядок, число тощо)
        
    Returns:
        str: JSON-рядок, що представляє вхідний об'єкт
    """
    data: bytes = bytes_encode(obj)
    return data.decode()
