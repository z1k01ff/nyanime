from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook import aiohttp_server as server
from aiohttp import web

if TYPE_CHECKING:
    from app.models.config import AppConfig


async def polling_startup(bots: list[Bot], config: AppConfig) -> None:
    """
    Функція запуску для режиму polling.
    
    Видаляє вебхуки для всіх ботів та опціонально пропускає накопичені оновлення.
    
    Args:
        bots: Список ботів для налаштування
        config: Конфігурація додатку
    """
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=config.telegram.drop_pending_updates)
    if config.telegram.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    """
    Функція запуску для режиму webhook.
    
    Налаштовує вебхук для бота з параметрами з конфігурації.
    
    Args:
        dispatcher: Диспетчер Aiogram
        bot: Екземпляр бота для налаштування
        config: Конфігурація додатку
        
    Returns:
        Логування результату встановлення вебхука
    """
    # Формуємо URL для вебхука на основі конфігурації
    url: str = config.server.build_url(path=config.telegram.webhook_path)
    
    # Встановлюємо вебхук з необхідними параметрами
    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.telegram.webhook_secret.get_secret_value(),
        drop_pending_updates=config.telegram.drop_pending_updates,
    ):
        return loggers.webhook.info("Main bot webhook successfully set on url '%s'", url)
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, config: AppConfig) -> None:
    """
    Функція завершення роботи для режиму webhook.
    
    Видаляє вебхук бота, якщо це вказано в конфігурації, та закриває сесію.
    
    Args:
        bot: Екземпляр бота
        config: Конфігурація додатку
    """
    # Пропускаємо видалення вебхука, якщо це не вказано в конфігурації
    if not config.telegram.reset_webhook:
        return
        
    # Видаляємо вебхук та логуємо результат
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop main bot webhook.")
        
    # Закриваємо сесію бота
    await bot.session.close()


def run_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    """
    Запускає бота в режимі polling.
    
    Реєструє функцію запуску та запускає polling.
    
    Args:
        dispatcher: Диспетчер Aiogram
        bot: Екземпляр бота
    """
    # Реєструємо функцію запуску
    dispatcher.startup.register(polling_startup)
    # Запускаємо polling
    return dispatcher.run_polling(bot)


def run_webhook(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    """
    Запускає бота в режимі webhook.
    
    Налаштовує aiohttp-сервер для обробки вебхуків та запускає його.
    
    Args:
        dispatcher: Диспетчер Aiogram
        bot: Екземпляр бота
        config: Конфігурація додатку
    """
    # Створюємо aiohttp-додаток
    app: web.Application = web.Application()
    
    # Налаштовуємо обробник вебхуків
    server.SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=config.telegram.webhook_secret.get_secret_value(),
    ).register(app, path=config.telegram.webhook_path)
    
    # Налаштовуємо додаток для роботи з диспетчером
    server.setup_application(app, dispatcher, bot=bot)
    app.update(**dispatcher.workflow_data, bot=bot)
    
    # Реєструємо функції запуску та завершення роботи
    dispatcher.startup.register(webhook_startup)
    dispatcher.shutdown.register(webhook_shutdown)
    
    # Запускаємо веб-сервер
    return web.run_app(
        app=app,
        host=config.server.host,
        port=config.server.port,
    )
