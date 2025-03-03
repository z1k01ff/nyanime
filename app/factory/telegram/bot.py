from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.contrib.middlewares import RetryRequestMiddleware
from aiogram.enums import ParseMode

from app.utils import mjson

if TYPE_CHECKING:
    from app.models.config import AppConfig


def create_bot(config: AppConfig) -> Bot:
    """
    Створює та налаштовує екземпляр бота Telegram.
    
    Функція ініціалізує сесію для HTTP-запитів з власними функціями
    кодування/декодування JSON, додає middleware для повторних спроб
    при помилках та створює бота з налаштуваннями з конфігурації.
    
    Args:
        config: Об'єкт конфігурації додатку, що містить токен бота
               та інші налаштування для Telegram
               
    Returns:
        Налаштований екземпляр бота Telegram, готовий до використання
    """
    # Створюємо сесію для HTTP-запитів з власними функціями для роботи з JSON
    session: AiohttpSession = AiohttpSession(
        json_loads=mjson.decode,  # Функція для декодування JSON
        json_dumps=mjson.encode,  # Функція для кодування JSON
    )
    
    # Додаємо middleware для автоматичних повторних спроб при помилках мережі
    session.middleware(RetryRequestMiddleware())
    
    # Створюємо та повертаємо екземпляр бота з налаштуваннями
    return Bot(
        # Токен бота з конфігурації (отримуємо секретне значення)
        token=config.telegram.bot_token.get_secret_value(),
        # Використовуємо налаштовану сесію
        session=session,
        # Встановлюємо HTML як формат розбору повідомлень за замовчуванням
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
