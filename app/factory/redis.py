from __future__ import annotations

from redis.asyncio import ConnectionPool, Redis


def create_redis(url: str) -> Redis:
    """
    Створює та повертає асинхронний клієнт Redis.
    
    Функція ініціалізує підключення до Redis за допомогою наданого URL
    та створює пул з'єднань для ефективного використання ресурсів.
    
    Args:
        url: URL-адреса для підключення до Redis у форматі 
             "redis://[[username]:[password]]@host:port/db"
             
    Returns:
        Асинхронний клієнт Redis з налаштованим пулом з'єднань
    """
    # Створюємо пул з'єднань з Redis за вказаним URL
    # та ініціалізуємо клієнт Redis з цим пулом
    return Redis(connection_pool=ConnectionPool.from_url(url=url))
