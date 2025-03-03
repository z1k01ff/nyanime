"""
Модуль з патчами та розширеннями для бібліотеки Fluent.

Цей модуль містить класи, які розширюють функціональність бібліотеки Fluent
для локалізації, додаючи підтримку нових типів даних та змінюючи налаштування
форматування за замовчуванням.
"""

from typing import Any, Optional

from fluent.runtime.types import FluentNumber, FluentType, NumberFormatOptions

# Змінюємо налаштування форматування чисел за замовчуванням,
# щоб вимкнути групування цифр (розділення тисяч)
FluentNumber.default_number_format_options = NumberFormatOptions(useGrouping=False)


class FluentBool(FluentType):
    """
    Клас для представлення булевих значень у Fluent.
    
    Цей клас дозволяє використовувати булеві значення (True/False) у локалізаційних
    файлах Fluent, перетворюючи їх на рядки "true" або "false".
    
    Attributes:
        value: Булеве значення, яке представляє цей об'єкт
    """
    
    def __init__(self, value: Any) -> None:
        """
        Ініціалізує об'єкт FluentBool з вказаним значенням.
        
        Args:
            value: Будь-яке значення, яке буде перетворено на булеве
        """
        self.value = bool(value)

    def format(self, *_: Any) -> str:
        """
        Форматує булеве значення як рядок.
        
        Returns:
            str: "true" якщо значення True, інакше "false"
        """
        if self.value:
            return "true"
        return "false"

    def __eq__(self, other: object) -> bool:
        """
        Перевіряє рівність з іншим об'єктом.
        
        Args:
            other: Об'єкт для порівняння
            
        Returns:
            bool: True, якщо other є рядком, рівним форматованому значенню цього об'єкта
        """
        if isinstance(other, str):
            return self.format() == other
        return False


class FluentNullable(FluentType):
    """
    Клас для представлення значень, які можуть бути None, у Fluent.
    
    Цей клас дозволяє безпечно використовувати значення, які можуть бути None,
    у локалізаційних файлах Fluent, перетворюючи None на рядок "null".
    
    Attributes:
        value: Значення, яке може бути None
    """
    
    def __init__(self, value: Optional[Any] = None) -> None:
        """
        Ініціалізує об'єкт FluentNullable з вказаним значенням.
        
        Args:
            value: Будь-яке значення, включаючи None
        """
        self.value = value

    def format(self, *_: Any) -> str:
        """
        Форматує значення як рядок.
        
        Returns:
            str: Рядкове представлення значення або "null", якщо значення None
        """
        if self.value is not None:
            return str(self.value)
        return "null"

    def __eq__(self, other: object) -> bool:
        """
        Перевіряє рівність з іншим об'єктом.
        
        Args:
            other: Об'єкт для порівняння
            
        Returns:
            bool: True, якщо other є рядком, рівним форматованому значенню цього об'єкта
        """
        if isinstance(other, str):
            return self.format() == other
        return False
