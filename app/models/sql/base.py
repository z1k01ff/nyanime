from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger
from sqlalchemy.orm import DeclarativeBase, registry

from app.utils.custom_types import Int16, Int32, Int64


class Base(DeclarativeBase):
    """
    Базовий клас для всіх моделей SQLAlchemy в додатку.
    
    Цей клас є основою для всіх ORM-моделей в системі та визначає
    спільну конфігурацію, включаючи відображення типів даних Python
    на типи даних SQL. Успадковує DeclarativeBase з SQLAlchemy.
    
    Attributes:
        registry: Реєстр метаданих SQLAlchemy з налаштованим відображенням
                 типів даних Python на типи даних SQL.
    """
    
    # Реєстр метаданих SQLAlchemy з відображенням типів
    registry = registry(
        type_annotation_map={
            # Відображення користувацьких типів на типи SQL
            Int16: SmallInteger,  # 16-бітне ціле число -> SMALLINT
            Int32: Integer,       # 32-бітне ціле число -> INTEGER
            Int64: BigInteger,    # 64-бітне ціле число -> BIGINT
            
            # Відображення стандартних типів Python
            datetime: DateTime(timezone=True),  # datetime -> TIMESTAMP WITH TIME ZONE
        }
    )
