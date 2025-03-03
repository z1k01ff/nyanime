from typing import Any

from app.utils.key_builder import StorageKey


class UserKey(StorageKey, prefix="users"):
    """
    Клас для генерації ключів Redis, пов'язаних з користувачами.
    
    Цей клас успадковує StorageKey і використовується для створення
    стандартизованих ключів для зберігання даних користувачів у Redis.
    Всі ключі мають префікс "users", що дозволяє легко ідентифікувати
    та групувати записи, пов'язані з користувачами.
    
    Attributes:
        key: Значення, яке буде додано до префіксу для формування повного ключа.
             Зазвичай це ідентифікатор користувача (telegram_id).
    
    Examples:
        >>> user_key = UserKey(key=123456789)
        >>> str(user_key)
        'users:123456789'
    """
    
    key: Any  # Значення ключа (зазвичай telegram_id користувача)
