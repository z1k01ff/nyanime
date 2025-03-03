"""
Модуль з константами для використання в усьому додатку.

Цей модуль містить глобальні константи, які використовуються в різних
частинах додатку, включаючи налаштування часового поясу, локалізації
та шляхи до важливих файлів і директорій.
"""

from datetime import timezone
from pathlib import Path
from typing import Final

from .enums import Locale

# Часовий пояс за замовчуванням для всіх операцій з датою та часом
TIMEZONE: Final[timezone] = timezone.utc

# Мова за замовчуванням для інтерфейсу бота
DEFAULT_LOCALE: Final[str] = Locale.EN

# Шлях до кореневої директорії проекту
ROOT_DIR: Final[Path] = Path(__file__).parent.parent

# Шлях до файлу з змінними середовища
ENV_FILE: Final[Path] = ROOT_DIR / ".env"

# Шлях до директорії з ресурсами
ASSETS_SOURCE_DIR: Final[Path] = ROOT_DIR / "assets"

# Шлях до директорії з файлами локалізації
MESSAGES_SOURCE_DIR: Final[Path] = ASSETS_SOURCE_DIR / "messages"
