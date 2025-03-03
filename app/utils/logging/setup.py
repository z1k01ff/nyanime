"""
Модуль для налаштування системи логування в додатку.

Цей модуль містить функції для налаштування логерів, включаючи
форматування повідомлень та рівні логування для різних компонентів.
"""

import logging


def disable_aiogram_logs() -> None:
    """
    Вимикає детальне логування для деяких модулів aiogram.
    
    Ця функція встановлює рівень логування WARNING для модулів aiogram,
    які генерують багато повідомлень, щоб зменшити шум у логах.
    """
    for name in ["aiogram.middlewares", "aiogram.event", "aiohttp.access"]:
        logging.getLogger(name).setLevel(logging.WARNING)


def setup_logger(level: int = logging.INFO) -> None:
    """
    Налаштовує основний логер додатку.
    
    Встановлює базову конфігурацію логування, включаючи формат повідомлень,
    формат часу та рівень логування.
    
    Args:
        level: Рівень логування (за замовчуванням logging.INFO)
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=level,
    )
