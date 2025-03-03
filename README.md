# aiogram_bot_template
[![Автор](https://img.shields.io/badge/Author-@wakaree-blue)](https://wakaree.dev)
[![Ліцензія](https://img.shields.io/badge/License-MIT-blue)](#license)

## ⚙️ Системні залежності
- Python 3.11+
- Docker
- docker-compose
- make
- uv

## 🐳 Швидкий старт з Docker compose
- Перейменуйте `.env.dist` на `.env` та налаштуйте його
- Перейменуйте `docker-compose.example.yml` на `docker-compose.yml`
- Виконайте команду `make app-build`, а потім `make app-run`, щоб запустити бота

Використовуйте `make`, щоб побачити всі доступні команди

## 🔧 Розробка

### Налаштування середовища
```bash
uv sync
```
### Оновлення структури таблиць бази даних
**Створення скрипту міграції:**
```bash
make migration message=ПОВІДОМЛЕННЯ_ЩО_РОБИТЬ_МІГРАЦІЯ
```
**Запуск міграцій:**
```bash
make migrate
```

## 🚀 Використані технології:
- [uv](https://docs.astral.sh/uv/) (надзвичайно швидкий менеджер пакетів та проектів Python)
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (фреймворк для Telegram ботів)
- [PostgreSQL](https://www.postgresql.org/) (реляційна база даних)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (робота з базою даних з Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (легкий інструмент для міграції баз даних)
- [Redis](https://redis.io/docs/) (база даних в пам'яті для FSM та кешування)
- [Project Fluent](https://projectfluent.org/) (сучасна система локалізації)

## 🤝 Внески

### 🐛 Звіти про помилки / ✨ Запити на нові функції

Якщо ви хочете повідомити про помилку або запросити нову функцію, не соромтеся відкрити [нове питання](https://github.com/wakaree/aiogram_bot_template/issues/new).

### Pull Requests

Якщо ви хочете допомогти нам покращити бота, ви можете створити новий [Pull Request](https://github.com/wakaree/aiogram_bot_template/pulls).

## 📝 Ліцензія

Цей проект ліцензований за ліцензією MIT - дивіться файл [LICENSE](LICENSE) для деталей.
