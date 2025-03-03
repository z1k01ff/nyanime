#!/bin/bash
# 
# Скрипт для вилучення рядків локалізації з коду проекту.
# 
# Цей скрипт автоматично вилучає всі рядки локалізації з коду проекту
# та генерує файли .ftl для кожної підтримуваної мови.
# Використовує утиліту ftl-extract для аналізу коду.

# Завантаження всіх локалей з файлу .env
CURRENT_LOCALES=$(grep '^TELEGRAM_LOCALES=' ./.env | cut -d '=' -f 2)

# Ініціалізація порожньої змінної для оброблених локалей
PROCESSED_LOCALES=""

# Встановлення роздільника для розділення локалей комою
IFS=','

# Цикл по кожній локалі в CURRENT_LOCALES
for lang in $CURRENT_LOCALES; do
    # Додавання кожної локалі до PROCESSED_LOCALES з роздільником пробілу
    PROCESSED_LOCALES="$PROCESSED_LOCALES -l $lang"
done

# Скидання IFS до значення за замовчуванням
unset IFS

# Видалення першого символу (пробілу)
PROCESSED_LOCALES="${PROCESSED_LOCALES#?}"

# Запуск скрипту з обробленими локалями як аргументами
# shellcheck disable=SC2086
uv run ftl-extract \
    app assets/messages \
    --default-ftl-file messages.ftl $PROCESSED_LOCALES
