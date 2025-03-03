from __future__ import annotations

from typing import Any, Optional, TypeVar, Union, cast

from sqlalchemy import ColumnExpressionArgument, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from ..uow import UoW

# Типовий параметр для моделей даних
T = TypeVar("T", bound=Any)
# Тип для колонок SQL-запитів
ColumnClauseType = Union[
    type[T],
    InstrumentedAttribute[T],
]


# noinspection PyTypeChecker
class BaseRepository:
    """
    Базовий клас репозиторію для роботи з SQL-моделями.
    
    Надає основні методи для отримання, оновлення та видалення даних.
    Використовує SQLAlchemy для взаємодії з базою даних.
    """
    session: AsyncSession
    uow: UoW

    def __init__(self, session: AsyncSession) -> None:
        """
        Ініціалізує репозиторій з асинхронною сесією SQLAlchemy.
        
        Args:
            session: Асинхронна сесія SQLAlchemy для виконання запитів до бази даних
        """
        self.session = session
        self.uow = UoW(session=session)

    async def _get(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> Optional[T]:
        """
        Отримує один запис з бази даних за вказаними умовами.
        
        Args:
            model: Модель даних або атрибут моделі для вибірки
            conditions: Умови фільтрації запитів (WHERE)
            
        Returns:
            Об'єкт моделі або None, якщо запис не знайдено
        """
        return cast(Optional[T], await self.session.scalar(select(model).where(*conditions)))

    async def _get_many(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> list[T]:
        """
        Отримує список записів з бази даних за вказаними умовами.
        
        Args:
            model: Модель даних або атрибут моделі для вибірки
            conditions: Умови фільтрації запитів (WHERE)
            
        Returns:
            Список об'єктів моделі, що відповідають умовам
        """
        return list(await self.session.scalars(select(model).where(*conditions)))

    async def _update(
        self,
        model: ColumnClauseType[T],
        conditions: list[ColumnExpressionArgument[Any]],
        load_result: bool = True,
        **kwargs: Any,
    ) -> Optional[T]:
        """
        Оновлює записи в базі даних за вказаними умовами.
        
        Args:
            model: Модель даних або атрибут моделі для оновлення
            conditions: Умови фільтрації запитів (WHERE)
            load_result: Чи повертати оновлений об'єкт
            kwargs: Пари ключ-значення для оновлення полів
            
        Returns:
            Оновлений об'єкт моделі або None, якщо load_result=False
        """
        # Якщо немає даних для оновлення, просто повертаємо поточний запис або None
        if not kwargs:
            if not load_result:
                return None
            return cast(Optional[T], await self._get(model, *conditions))
        
        # Формуємо запит на оновлення
        query = update(model).where(*conditions).values(**kwargs)
        if load_result:
            query = query.returning(model)
            
        # Виконуємо запит та зберігаємо зміни
        result = await self.session.execute(query)
        await self.session.commit()
        
        return result.scalar_one_or_none() if load_result else None

    async def _delete(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> bool:
        """
        Видаляє записи з бази даних за вказаними умовами.
        
        Args:
            model: Модель даних або атрибут моделі для видалення
            conditions: Умови фільтрації запитів (WHERE)
            
        Returns:
            True, якщо був видалений хоча б один запис, інакше False
        """
        result = await self.session.execute(delete(model).where(*conditions))
        await self.session.commit()
        return cast(bool, result.rowcount > 0)
