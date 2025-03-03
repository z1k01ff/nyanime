import asyncio
from types import TracebackType
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .repositories import Repository
from .uow import UoW


class SQLSessionContext:
    """
    Контекст сесії SQL для керування з'єднанням з базою даних.
    
    Цей клас реалізує асинхронний контекстний менеджер для безпечної роботи
    з базою даних. Він автоматично створює сесію при вході в контекст
    та закриває її при виході, навіть у випадку виникнення винятків.
    
    Приклад використання:
        async with SQLSessionContext(session_pool) as (repo, uow):
            user = await repo.users.get_by_id(user_id)
            user.name = "Нове ім'я"
            await uow.commit()
    """
    
    # _session_pool - це "фабрика" для створення сесій бази даних
    # _session - це поточна активна сесія (з'єднання з базою даних)
    _session_pool: async_sessionmaker[AsyncSession]
    _session: Optional[AsyncSession]

    # __slots__ - це оптимізація Python для зменшення використання пам'яті
    __slots__ = ("_session_pool", "_session")

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]) -> None:
        """
        Ініціалізує контекст сесії SQL.
        
        Args:
            session_pool: Фабрика для створення асинхронних сесій SQLAlchemy.
        """
        # Конструктор класу, який приймає пул сесій
        # Ми зберігаємо пул, але не створюємо сесію одразу
        self._session_pool = session_pool
        self._session = None

    async def __aenter__(self) -> tuple[Repository, UoW]:
        """
        Створює нову сесію та повертає репозиторій і UoW.
        
        Returns:
            Кортеж з двох об'єктів:
            - Repository: для виконання запитів до бази даних
            - UoW: для керування транзакціями та збереження змін
        """
        # Цей метод викликається, коли ми входимо в блок "async with"
        # Наприклад: async with SQLSessionContext(...) as (repo, uow):
        
        # Створюємо нову сесію з пулу
        self._session = await self._session_pool().__aenter__()
        
        # Повертаємо два об'єкти:
        # 1. Repository - для отримання даних з бази (SELECT запити)
        # 2. UoW (Unit of Work) - для збереження змін (INSERT, UPDATE, DELETE)
        return Repository(session=self._session), UoW(session=self._session)

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """
        Закриває сесію при виході з контексту.
        
        Args:
            exc_type: Тип винятку, якщо він виник
            exc_value: Об'єкт винятку, якщо він виник
            traceback: Об'єкт трасування, якщо виник виняток
        """
        # Цей метод викликається, коли ми виходимо з блоку "async with"
        # Він відповідає за закриття сесії та звільнення ресурсів
        
        # Якщо сесія не була створена, нічого не робимо
        if self._session is None:
            return
            
        # Створюємо асинхронну задачу для закриття сесії
        # Це дозволяє не блокувати основний потік виконання
        task: asyncio.Task[None] = asyncio.create_task(self._session.close())
        
        # asyncio.shield захищає задачу від скасування
        # Це гарантує, що сесія буде закрита навіть при помилках
        await asyncio.shield(task)
        
        # Очищаємо посилання на сесію
        self._session = None

# Приклад використання (не є частиною файлу):
#
# async def get_user(user_id: int):
#     async with SQLSessionContext(session_pool) as (repo, uow):
#         # Використовуємо репозиторій для отримання даних
#         user = await repo.users.get_by_id(user_id)
#         
#         # Змінюємо дані
#         user.name = "Нове ім'я"
#         
#         # Зберігаємо зміни через Unit of Work
#         await uow.commit()
#         
#         return user
