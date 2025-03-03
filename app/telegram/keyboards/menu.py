"""
Модуль для створення клавіатур меню Telegram бота.

Цей модуль містить функції для генерації різних типів клавіатур,
які використовуються в меню бота.
"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from .callback_data.menu import CDPing


def ping_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    """
    Створює клавіатуру з кнопкою "ping".
    
    Ця клавіатура містить одну кнопку, яка при натисканні відправляє callback-запит
    з даними CDPing.
    
    Args:
        i18n: Контекст інтернаціоналізації для перекладу тексту кнопки
        
    Returns:
        InlineKeyboardMarkup: Готова клавіатура з кнопкою "ping"
    """
    # Створення будівельника клавіатури
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Додавання кнопки з перекладеним текстом та callback-даними
    builder.button(text=i18n.buttons.ping(_path="menu.ftl"), callback_data=CDPing())
    # Повернення готової клавіатури
    return builder.as_markup()
