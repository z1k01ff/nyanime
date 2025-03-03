from .base import EnvSettings


class ServerConfig(EnvSettings, env_prefix="SERVER_"):
    """
    Конфігурація для веб-сервера додатку.
    
    Цей клас містить налаштування для веб-сервера, який використовується
    для режиму webhook при роботі з Telegram API. Завантажує значення
    з змінних середовища з префіксом SERVER_.
    
    Attributes:
        port: Порт, на якому буде запущено веб-сервер.
              Завантажується з SERVER_PORT.
        host: Хост, на якому буде запущено веб-сервер.
              Завантажується з SERVER_HOST.
        url: Публічна URL-адреса сервера, яка використовується для
             налаштування вебхуків. Завантажується з SERVER_URL.
    """
    
    port: int  # Порт для веб-сервера
    host: str  # Хост для веб-сервера
    url: str   # Публічна URL-адреса сервера

    def build_url(self, path: str) -> str:
        """
        Створює повну URL-адресу для вказаного шляху.
        
        Метод об'єднує базову URL-адресу сервера з вказаним шляхом,
        що дозволяє формувати повні URL для різних ендпоінтів.
        
        Args:
            path: Шлях, який потрібно додати до базової URL-адреси.
                 Може починатися з "/" або без нього.
                 
        Returns:
            str: Повна URL-адреса, що складається з базової URL та вказаного шляху.
        
        Examples:
            >>> config = ServerConfig(port=8080, host="localhost", url="https://example.com")
            >>> config.build_url("/webhook")
            'https://example.com/webhook'
        """
        return f"{self.url}{path}"
