"""
Модуль, що містить базовий клас для типізованих проміжних обробників подій.

Цей модуль надає абстрактний базовий клас для створення проміжних обробників,
які можуть бути налаштовані для роботи з конкретними типами подій Telegram.
"""

from abc import ABC
from typing import ClassVar, Final

from aiogram import BaseMiddleware, Router

from app.enums import MiddlewareEventType

# Список типів подій, які обробляються за замовчуванням
DEFAULT_UPDATE_TYPES: Final[list[MiddlewareEventType]] = [
    MiddlewareEventType.MESSAGE,
    MiddlewareEventType.CALLBACK_QUERY,
    MiddlewareEventType.MY_CHAT_MEMBER,
    MiddlewareEventType.ERROR,
    MiddlewareEventType.INLINE_QUERY,
]


class EventTypedMiddleware(BaseMiddleware, ABC):
    """
    Абстрактний базовий клас для проміжних обробників з типізацією подій.
    
    Цей клас дозволяє створювати проміжні обробники, які автоматично
    реєструються для обробки конкретних типів подій Telegram.
    
    Attributes:
        __event_types__: Список типів подій, для яких буде зареєстрований обробник.
                         За замовчуванням використовується DEFAULT_UPDATE_TYPES.
    """
    __event_types__: ClassVar[list[MiddlewareEventType]] = DEFAULT_UPDATE_TYPES

    def setup_inner(self, router: Router) -> None:
        """
        Реєструє проміжний обробник як внутрішній для вказаних типів подій.
        
        Внутрішні обробники викликаються після фільтрів, але перед основними обробниками.
        
        Args:
            router: Маршрутизатор, в якому реєструється проміжний обробник
        """
        for event_type in self.__event_types__:
            router.observers[event_type].middleware(self)

    def setup_outer(self, router: Router) -> None:
        """
        Реєструє проміжний обробник як зовнішній для вказаних типів подій.
        
        Зовнішні обробники викликаються перед фільтрами та основними обробниками.
        
        Args:
            router: Маршрутизатор, в якому реєструється проміжний обробник
        """
        for event_type in self.__event_types__:
            router.observers[event_type].outer_middleware(self)
