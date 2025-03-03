"""
Модуль для обробки адміністративних команд та запитів у Telegram боті.

Цей модуль містить маршрутизатор для обробки повідомлень та callback-запитів,
які надходять від адміністраторів бота. Всі обробники, зареєстровані в цьому
маршрутизаторі, будуть доступні тільки для користувачів з адміністративними правами.
"""

from typing import Final

from aiogram import Router

from app.telegram.filters import ADMIN_FILTER

# Створення маршрутизатора для адміністративних обробників
router: Final[Router] = Router(name=__name__)
# Застосування фільтра адміністратора до всіх повідомлень
router.message.filter(ADMIN_FILTER)
# Застосування фільтра адміністратора до всіх callback-запитів
router.callback_query.filter(ADMIN_FILTER)
