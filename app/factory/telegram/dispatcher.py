from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from redis.asyncio import Redis

from app.models.config import AppConfig
from app.services.database.redis import RedisRepository
from app.telegram.handlers import admin, common, extra
from app.telegram.middlewares import UserMiddleware
from app.utils import mjson

from ..redis import create_redis
from ..session_pool import create_session_pool
from .i18n import create_i18n_middleware


def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    Створює та налаштовує диспетчер Aiogram для обробки оновлень Telegram.
    
    Функція ініціалізує Redis-клієнт, налаштовує сховище для FSM (Finite State Machine),
    додає необхідні middleware та підключає маршрутизатори з обробниками повідомлень.
    
    Args:
        config: Об'єкт конфігурації додатку з налаштуваннями для Redis, бази даних та ін.
        
    Returns:
        Налаштований диспетчер Aiogram з усіма необхідними компонентами
    """
    # Створюємо клієнт Redis для сховища станів та репозиторію
    redis: Redis = create_redis(url=config.redis.build_url())
    
    # Створюємо middleware для інтернаціоналізації
    i18n_middleware: I18nMiddleware = create_i18n_middleware(config)

    # Створюємо та налаштовуємо диспетчер
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",  # Ім'я диспетчера для логування
        # Сховище для FSM на основі Redis з власними функціями для JSON
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        config=config,  # Передаємо конфігурацію для доступу в обробниках
        # Створюємо пул сесій для роботи з базою даних
        session_pool=create_session_pool(config=config),
        # Репозиторій Redis для кешування та зберігання даних
        redis=RedisRepository(client=redis),
    )

    # Підключаємо маршрутизатори з обробниками повідомлень
    dispatcher.include_routers(admin.router, common.router, extra.router)
    
    # Додаємо middleware для роботи з користувачами
    dispatcher.update.outer_middleware(UserMiddleware())
    
    # Налаштовуємо middleware для інтернаціоналізації
    i18n_middleware.setup(dispatcher=dispatcher)
    
    # Додаємо middleware для автоматичної відповіді на callback-запити
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    return dispatcher
