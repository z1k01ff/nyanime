from pydantic import SecretStr
from sqlalchemy import URL

from .base import EnvSettings


class PostgresConfig(EnvSettings, env_prefix="POSTGRES_"):
    """
    Конфігурація для підключення до бази даних PostgreSQL.
    
    Цей клас містить всі необхідні параметри для встановлення з'єднання
    з базою даних PostgreSQL. Завантажує значення з змінних середовища
    з префіксом POSTGRES_.
    
    Attributes:
        host: Хост сервера PostgreSQL. Завантажується з POSTGRES_HOST.
        db: Назва бази даних. Завантажується з POSTGRES_DB.
        password: Пароль для підключення до бази даних, зберігається як SecretStr
                для безпеки. Завантажується з POSTGRES_PASSWORD.
        port: Порт сервера PostgreSQL. Завантажується з POSTGRES_PORT.
        user: Ім'я користувача для підключення. Завантажується з POSTGRES_USER.
        data: Додаткові дані для підключення. Завантажується з POSTGRES_DATA.
    """
    
    host: str  # Хост сервера PostgreSQL
    db: str  # Назва бази даних
    password: SecretStr  # Пароль (зберігається як SecretStr для безпеки)
    port: int  # Порт сервера PostgreSQL
    user: str  # Ім'я користувача
    data: str  # Додаткові дані для підключення

    def build_url(self) -> URL:
        """
        Створює URL для підключення до бази даних PostgreSQL.
        
        Метод формує URL-об'єкт SQLAlchemy з параметрами підключення,
        який використовується для створення з'єднання з базою даних.
        
        Returns:
            URL: Об'єкт URL SQLAlchemy для підключення до PostgreSQL
                з використанням драйвера asyncpg.
        """
        return URL.create(
            drivername="postgresql+asyncpg",  # Асинхронний драйвер для PostgreSQL
            username=self.user,  # Ім'я користувача
            password=self.password.get_secret_value(),  # Отримуємо значення пароля з SecretStr
            host=self.host,  # Хост сервера
            port=self.port,  # Порт сервера
            database=self.db,  # Назва бази даних
        )
