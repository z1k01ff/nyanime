"""
Головний модуль запуску Telegram бота.

Цей модуль містить точку входу в програму та відповідає за ініціалізацію
та запуск бота з відповідними налаштуваннями.
"""

from aiogram import Bot, Dispatcher

from .factory import create_app_config, create_bot, create_dispatcher
from .models.config import AppConfig
from .runners import run_polling, run_webhook
from .utils.logging import setup_logger


def main() -> None:
    """
    Головна функція запуску бота.
    
    Ця функція виконує наступні кроки:
    1. Налаштовує систему логування
    2. Створює конфігурацію додатку
    3. Ініціалізує диспетчер та бота
    4. Запускає бота в режимі webhook або polling залежно від конфігурації
    
    Returns:
        None
    """
    # Налаштування системи логування
    setup_logger()
    
    # Створення конфігурації додатку з файлів або змінних середовища
    config: AppConfig = create_app_config()
    
    # Ініціалізація диспетчера з налаштуваннями
    dispatcher: Dispatcher = create_dispatcher(config=config)
    
    # Створення екземпляра бота з токеном та налаштуваннями
    bot: Bot = create_bot(config=config)
    
    # Вибір режиму запуску бота (webhook або polling)
    if config.telegram.use_webhook:
        return run_webhook(dispatcher=dispatcher, bot=bot, config=config)
    return run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
