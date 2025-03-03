from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, PrivateAttr


class PydanticModel(_BaseModel):
    """
    Базова модель Pydantic для всіх DTO (Data Transfer Objects) в додатку.
    
    Цей клас розширює стандартну BaseModel з Pydantic, додаючи функціональність
    для відстеження змінених полів та налаштовуючи поведінку валідації.
    Використовується як основа для всіх моделей передачі даних в системі.
    
    Attributes:
        model_config: Конфігурація Pydantic для моделі, яка визначає:
            - extra="ignore": Ігнорувати додаткові поля при валідації
            - from_attributes=True: Дозволяє створювати моделі з атрибутів об'єктів
              (наприклад, з ORM-моделей SQLAlchemy)
        __updated: Приватний атрибут для зберігання змінених полів та їх значень.
                  Доступний через властивість model_state.
    """
    
    model_config = ConfigDict(
        extra="ignore",  # Ігнорувати додаткові поля при валідації
        from_attributes=True,  # Дозволяє створювати моделі з атрибутів об'єктів
    )

    # Приватний атрибут для зберігання змінених полів та їх значень
    __updated: dict[str, Any] = PrivateAttr(default_factory=dict)

    @property
    def model_state(self) -> dict[str, Any]:
        """
        Повертає словник змінених полів та їх значень.
        
        Ця властивість надає доступ до приватного атрибута __updated,
        який містить інформацію про всі поля, що були змінені після
        створення об'єкта.
        
        Returns:
            dict[str, Any]: Словник, де ключі - назви змінених полів,
                           а значення - нові значення цих полів.
        """
        return self.__updated

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Перевизначений метод для встановлення значень атрибутів.
        
        Цей метод розширює стандартну поведінку __setattr__, додаючи
        відстеження змінених полів. При кожному встановленні значення
        атрибута, це значення також зберігається в словнику __updated.
        
        Args:
            name: Назва атрибута, який встановлюється.
            value: Нове значення атрибута.
        """
        super().__setattr__(name, value)
        self.__updated[name] = value
