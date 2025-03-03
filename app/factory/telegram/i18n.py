from __future__ import annotations

from typing import cast

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app.const import DEFAULT_LOCALE, MESSAGES_SOURCE_DIR
from app.models.config import AppConfig
from app.utils.localization import UserManager


def create_i18n_core(config: AppConfig) -> FluentRuntimeCore:
    """
    Створює та налаштовує ядро для інтернаціоналізації на основі Fluent.
    
    Функція ініціалізує ядро FluentRuntimeCore з налаштуваннями шляху до
    файлів локалізації та карти локалей для резервного перекладу.
    
    Args:
        config: Об'єкт конфігурації додатку з налаштуваннями локалей
        
    Returns:
        Налаштоване ядро FluentRuntimeCore для роботи з перекладами
    """
    # Отримуємо список підтримуваних локалей з конфігурації
    locales: list[str] = cast(list[str], config.telegram.locales)
    
    # Створюємо та повертаємо ядро для інтернаціоналізації
    return FluentRuntimeCore(
        # Шлях до директорії з файлами локалізації
        # {locale} буде замінено на конкретну локаль (наприклад, "uk", "en")
        path=MESSAGES_SOURCE_DIR / "{locale}",
        
        # Не викидати помилку, якщо ключ перекладу не знайдено
        raise_key_error=False,
        
        # Карта локалей для резервного перекладу
        # Якщо переклад не знайдено в поточній локалі, буде використано наступну
        # Наприклад, якщо locales = ["uk", "en", "de"], то:
        # - для "uk" резервною буде "en"
        # - для "en" резервною буде "de"
        locales_map={locales[i]: locales[i + 1] for i in range(len(locales) - 1)},
    )


def create_i18n_middleware(config: AppConfig) -> I18nMiddleware:
    """
    Створює та налаштовує middleware для інтернаціоналізації.
    
    Функція ініціалізує I18nMiddleware з ядром для інтернаціоналізації,
    менеджером користувачів для зберігання локалей та локаллю за замовчуванням.
    
    Args:
        config: Об'єкт конфігурації додатку з налаштуваннями локалей
        
    Returns:
        Налаштоване middleware для інтернаціоналізації
    """
    # Створюємо та повертаємо middleware для інтернаціоналізації
    return I18nMiddleware(
        # Ядро для роботи з перекладами
        core=create_i18n_core(config=config),
        
        # Менеджер для зберігання та отримання локалей користувачів
        manager=UserManager(),
        
        # Локаль за замовчуванням, яка буде використана,
        # якщо локаль користувача не визначена
        default_locale=DEFAULT_LOCALE,
    )
