from pydantic import BaseModel

from .common import CommonConfig
from .postgres import PostgresConfig
from .redis import RedisConfig
from .server import ServerConfig
from .sql_alchemy import SQLAlchemyConfig
from .telegram import TelegramConfig


class AppConfig(BaseModel):
    """
    Головна конфігурація додатку, що об'єднує всі конфігураційні компоненти.
    
    Цей клас агрегує всі окремі конфігураційні об'єкти в єдину структуру,
    що дозволяє зручно передавати конфігурацію між різними частинами додатку.
    Використовує Pydantic для валідації та завантаження конфігурації з
    змінних середовища.
    
    Attributes:
        telegram: Конфігурація для роботи з Telegram API (токени, налаштування вебхуків)
        postgres: Конфігурація для підключення до PostgreSQL бази даних
        sql_alchemy: Налаштування ORM SQLAlchemy (пул з'єднань, логування)
        redis: Конфігурація для підключення до Redis
        server: Налаштування веб-сервера для режиму webhook
        common: Загальні налаштування додатку (кешування, логування)
    """
    
    telegram: TelegramConfig
    postgres: PostgresConfig
    sql_alchemy: SQLAlchemyConfig
    redis: RedisConfig
    server: ServerConfig
    common: CommonConfig
