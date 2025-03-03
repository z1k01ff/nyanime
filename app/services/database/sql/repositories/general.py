from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .users import UsersRepository


class Repository(BaseRepository):
    """
    Головний репозиторій, який об'єднує всі інші репозиторії.
    
    Цей клас надає єдину точку доступу до всіх репозиторіїв у системі,
    що спрощує роботу з даними та забезпечує кращу організацію коду.
    Він наслідується від BaseRepository, щоб мати доступ до базових
    методів для роботи з базою даних.
    """
    
    # Репозиторій для роботи з користувачами
    users: UsersRepository

    def __init__(self, session: AsyncSession) -> None:
        """
        Ініціалізує головний репозиторій та всі підрепозиторії.
        
        Створює екземпляри всіх необхідних репозиторіїв, передаючи їм
        одну й ту саму сесію бази даних, щоб всі операції виконувались
        в рамках однієї транзакції.
        
        Args:
            session: Асинхронна сесія SQLAlchemy для взаємодії з базою даних
        """
        # Викликаємо конструктор базового класу, передаючи йому сесію
        super().__init__(session=session)
        
        # Ініціалізуємо репозиторій користувачів з тією ж сесією
        self.users = UsersRepository(session=session)
        
        # Тут можна додати інші репозиторії, наприклад:
        # self.products = ProductsRepository(session=session)
        # self.orders = OrdersRepository(session=session)
