from pydantic_settings import BaseSettings, SettingsConfigDict

from app.const import ENV_FILE


class EnvSettings(BaseSettings):
    """
    Базовий клас для всіх конфігураційних класів, що завантажують налаштування з середовища.
    
    Цей клас успадковує BaseSettings з pydantic_settings і надає спільну конфігурацію
    для всіх похідних класів налаштувань. Він визначає, як завантажувати змінні середовища,
    які файли .env використовувати та як обробляти додаткові поля.
    
    Attributes:
        model_config: Конфігурація для Pydantic, що визначає поведінку при завантаженні
                     налаштувань з середовища
    
    Notes:
        - Ігнорує додаткові поля, які не визначені в моделі
        - Завантажує змінні з файлу .env, шлях до якого визначено в ENV_FILE
        - Використовує UTF-8 кодування для файлу .env
    """
    
    model_config = SettingsConfigDict(
        extra="ignore",  # Ігнорувати додаткові поля, які не визначені в моделі
        env_file=ENV_FILE,  # Шлях до файлу .env з змінними середовища
        env_file_encoding="utf-8",  # Кодування файлу .env
    )
