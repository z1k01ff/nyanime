from pydantic import SecretStr

from .base import EnvSettings


class RedisConfig(EnvSettings, env_prefix="REDIS_"):
    """
    Конфігурація для підключення до сервера Redis.
    
    Цей клас містить всі необхідні параметри для встановлення з'єднання
    з сервером Redis. Завантажує значення з змінних середовища
    з префіксом REDIS_.
    
    Attributes:
        host: Хост сервера Redis. Завантажується з REDIS_HOST.
        password: Пароль для підключення до Redis, зберігається як SecretStr
                для безпеки. Завантажується з REDIS_PASSWORD.
        port: Порт сервера Redis. Завантажується з REDIS_PORT.
        db: Номер бази даних Redis. Завантажується з REDIS_DB.
        data: Додаткові дані для підключення. Завантажується з REDIS_DATA.
    """
    
    host: str  # Хост сервера Redis
    password: SecretStr  # Пароль (зберігається як SecretStr для безпеки)
    port: int  # Порт сервера Redis
    db: int  # Номер бази даних Redis
    data: str  # Додаткові дані для підключення

    def build_url(self) -> str:
        """
        Створює URL-рядок для підключення до сервера Redis.
        
        Метод формує URL-рядок з параметрами підключення у форматі,
        який використовується бібліотекою redis-py для встановлення з'єднання.
        
        Returns:
            str: URL-рядок для підключення до Redis у форматі
                 "redis://:[password]@[host]:[port]/[db]"
        """
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
