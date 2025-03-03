from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sql.base import Base


class UoW:
    """
    Unit of Work (Одиниця роботи) для керування транзакціями бази даних.
    
    Цей клас відповідає за збереження змін у базі даних, об'єднання об'єктів
    та видалення записів. Він інкапсулює логіку транзакцій та забезпечує
    атомарність операцій.
    
    Приклад використання:
        user = User(name="Іван", email="ivan@example.com")
        await uow.commit(user)
    """
    
    # Сесія SQLAlchemy для взаємодії з базою даних
    session: AsyncSession

    # __slots__ оптимізує використання пам'яті
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        """
        Ініціалізує Unit of Work з сесією бази даних.
        
        Args:
            session: Асинхронна сесія SQLAlchemy для взаємодії з базою даних
        """
        self.session = session

    async def commit(self, *instances: Base) -> None:
        """
        Додає об'єкти до сесії та зберігає зміни в базі даних.
        
        Цей метод додає всі передані об'єкти до сесії та виконує commit,
        зберігаючи всі зміни в базі даних в рамках однієї транзакції.
        
        Args:
            *instances: Об'єкти моделей SQLAlchemy для збереження
            
        Приклад:
            user1 = User(name="Іван")
            user2 = User(name="Марія")
            await uow.commit(user1, user2)
        """
        # Додаємо всі передані об'єкти до сесії
        self.session.add_all(instances)
        # Зберігаємо зміни в базі даних
        await self.session.commit()

    async def merge(self, *instances: Base) -> None:
        """
        Об'єднує стан об'єктів з базою даних.
        
        Метод merge використовується, коли об'єкт може вже існувати в базі даних.
        Він перевіряє наявність об'єкта і оновлює його, якщо він існує,
        або створює новий, якщо не існує.
        
        Args:
            *instances: Об'єкти моделей SQLAlchemy для об'єднання
            
        Приклад:
            user = User(id=1, name="Оновлене ім'я")  # id вже існує в БД
            await uow.merge(user)  # оновить існуючий запис
        """
        # Для кожного об'єкта виконуємо операцію merge
        for instance in instances:
            # merge перевіряє, чи існує об'єкт, і оновлює його або створює новий
            await self.session.merge(instance)

    async def delete(self, *instances: Base) -> None:
        """
        Видаляє об'єкти з бази даних.
        
        Цей метод позначає об'єкти як видалені та зберігає зміни,
        видаляючи відповідні записи з бази даних.
        
        Args:
            *instances: Об'єкти моделей SQLAlchemy для видалення
            
        Приклад:
            user = await repo.users.get(user_id=1)
            await uow.delete(user)
        """
        # Для кожного об'єкта виконуємо операцію видалення
        for instance in instances:
            # Позначаємо об'єкт як видалений
            await self.session.delete(instance)
        # Зберігаємо зміни (видалення) в базі даних
        await self.session.commit()
