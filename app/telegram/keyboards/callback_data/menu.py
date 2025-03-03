from aiogram.filters.callback_data import CallbackData


class CDPing(CallbackData, prefix="ping"):
    """
    Клас для обробки callback-даних пінг-запитів.
    
    Використовується для створення та обробки callback-даних,
    пов'язаних з функціональністю перевірки з'єднання (пінг).
    """
    pass