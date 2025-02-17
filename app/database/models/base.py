from datetime import datetime
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from typing_extensions import Annotated

# Визначення конвенції іменування для обмежень
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Створення метаданих з конвенцією іменування
metadata = MetaData(naming_convention=convention)

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=func.now())]


class Base(DeclarativeBase):
    metadata = metadata

    # Додаємо repr для кращого відображення об'єктів
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class TimestampMixin:
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class BaseModel(Base, TableNameMixin, TimestampMixin):
    __abstract__ = True

    id: Mapped[intpk]