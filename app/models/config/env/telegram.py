from pydantic import SecretStr

from app.utils.custom_types import StringList

from .base import EnvSettings


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    """
    Конфігурація для роботи з Telegram Bot API.
    
    Цей клас містить налаштування для взаємодії з Telegram API,
    включаючи токен бота, підтримувані мови, режим роботи (polling або webhook)
    та параметри вебхуків. Завантажує значення з змінних середовища
    з префіксом TELEGRAM_.
    
    Attributes:
        bot_token: Токен бота, отриманий від @BotFather. Зберігається як SecretStr
                  для безпеки. Завантажується з TELEGRAM_BOT_TOKEN.
        locales: Список підтримуваних мов (локалей) для інтернаціоналізації.
                Завантажується з TELEGRAM_LOCALES як список рядків, розділених комами.
        drop_pending_updates: Прапорець для пропуску накопичених оновлень при запуску бота.
                             Завантажується з TELEGRAM_DROP_PENDING_UPDATES.
        use_webhook: Прапорець для використання режиму webhook замість polling.
                    Завантажується з TELEGRAM_USE_WEBHOOK.
        reset_webhook: Прапорець для скидання вебхука при завершенні роботи бота.
                      Завантажується з TELEGRAM_RESET_WEBHOOK.
        webhook_path: Шлях для вебхука на сервері.
                     Завантажується з TELEGRAM_WEBHOOK_PATH.
        webhook_secret: Секретний токен для перевірки автентичності вебхуків.
                       Зберігається як SecretStr для безпеки.
                       Завантажується з TELEGRAM_WEBHOOK_SECRET.
    """
    
    bot_token: SecretStr  # Токен бота від @BotFather (зберігається як SecretStr для безпеки)
    locales: StringList  # Список підтримуваних мов (локалей)
    drop_pending_updates: bool  # Пропускати накопичені оновлення при запуску
    use_webhook: bool  # Використовувати webhook замість polling
    reset_webhook: bool  # Скидати вебхук при завершенні роботи
    webhook_path: str  # Шлях для вебхука на сервері
    webhook_secret: SecretStr  # Секретний токен для вебхуків (зберігається як SecretStr для безпеки)
