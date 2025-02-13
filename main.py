import asyncio
import logging
import sys
import warnings

from aiogram import Dispatcher, Bot, Router, F
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from aiogram_dialog.setup import DialogRegistry
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram.fsm.storage.memory import MemoryStorage

import app.handlers.user_task
from app.db_files.db_redis import redis
from app.dialogs.all_dialogs.menu_dialogs import main_menu_dialog
from app.dialogs.all_dialogs.new_user_dialogs import new_user_dialog
from app.dialogs.handlers import start_menu as start_menu_handler
from app.handlers import commands, photo, admin_task
from app.middleware.user import UserDatabaseMiddleware
from app.utils.bot import bot
from app.utils.scheduler import scheduler, scheduler_main
from app.utils.sync_to_async import cleanup  # Додайте цей імпорт
from app.dialogs.callbacks.pl_callbacks import check_pl_operations, edit_pl_operations

# Ігнорування warning dataframe_image
warnings.filterwarnings("ignore", category=FutureWarning)


storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
dp = Dispatcher(storage=storage)

# Вимкнення вбудованого логування SQLAlchemy
logging.disable(logging.WARNING)

callback_router = Router()
callback_router.callback_query.register(check_pl_operations, F.data.startswith("check_pl_"))

dp.update.middleware(UserDatabaseMiddleware(bot))

dp.include_router(start_menu_handler.router)
dp.include_router(commands.router)
dp.include_router(photo.router)
dp.include_router(app.handlers.user_task.router)
dp.include_router(app.handlers.admin_task.router)
dp.include_router(callback_router)

# Реєстрація діалогів у диспетчері
setup_dialogs(dp)
registry = DialogRegistry(dp)

dialogs = [
    new_user_dialog,
    main_menu_dialog,
]

for dialog in dialogs:
    dp.include_router(dialog)


async def shutdown() -> None:
    try:
        if scheduler and scheduler.running:
            scheduler.shutdown()
    except Exception as e:
        logger.error(f"Error during scheduler shutdown: {e}")
    await cleanup()  # Додаємо cleanup  від sync to async
    logger.info("Graceful shutdown completed.")


async def startup() -> None:
    scheduler.start()  # Запускаємо шедулер
    await scheduler_main(scheduler)  # Додаємо всі завдання
    logger.info("Graceful startup completed.")


async def main() -> None:
    try:
        await startup()
        me = await bot.get_me()
        logger.info(f"Dispatcher polling started:  {me.full_name}")
        await dp.start_polling(bot)
    finally:
        await shutdown()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")