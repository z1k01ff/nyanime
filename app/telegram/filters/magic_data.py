from typing import Any

from aiogram.filters import MagicData as _MagicData
from magic_filter import MagicFilter


class MagicData(_MagicData):
    """
    Розширений фільтр MagicData для перевірки даних у контексті обробників Aiogram.
    
    Цей клас успадковує базовий фільтр MagicData з Aiogram і додає додаткову
    перевірку типів для забезпечення коректної роботи з MagicFilter.
    """

    def __init__(self, magic_data: MagicFilter | Any) -> None:
        """
        Ініціалізує фільтр MagicData з перевіркою типу.
        
        Перевіряє, що переданий аргумент є екземпляром MagicFilter.
        Це необхідно, оскільки PyCharm може неправильно інтерпретувати
        вирази типу F.smth == F.smth2, вважаючи, що вони повертають bool.
        
        Args:
            magic_data: Об'єкт MagicFilter для фільтрації даних
            
        Raises:
            TypeError: Якщо переданий аргумент не є екземпляром MagicFilter
        """
        if not isinstance(magic_data, MagicFilter):
            raise TypeError(f"Expected MagicFilter got '{type(magic_data).__name__}'")
        super().__init__(magic_data=magic_data)
