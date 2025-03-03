"""
Модуль з користувацькими типами даних для використання в додатку.

Цей модуль містить визначення типів, які використовуються для анотацій
та валідації даних у різних частинах додатку.
"""

from typing import TYPE_CHECKING, Annotated, NewType, TypeAlias

from pydantic import PlainValidator

# Умовне визначення типу ListStr залежно від контексту виконання
if TYPE_CHECKING:
    # Під час перевірки типів використовуємо звичайний аліас типу
    ListStr: TypeAlias = list[str]
else:
    # Під час виконання використовуємо NewType для додаткової безпеки типів
    ListStr = NewType("ListStr", list[str])

# Тип для списку рядків, розділених комами
# Використовує PlainValidator для автоматичного перетворення рядка на список
StringList: TypeAlias = Annotated[ListStr, PlainValidator(func=lambda x: x.split(","))]

# Типи для цілих чисел різної розрядності
Int16: TypeAlias = Annotated[int, 16]  # 16-бітне ціле число
Int32: TypeAlias = Annotated[int, 32]  # 32-бітне ціле число
Int64: TypeAlias = Annotated[int, 64]  # 64-бітне ціле число
