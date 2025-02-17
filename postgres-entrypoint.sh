#!/bin/bash
# Створюємо pg_hba.conf якщо його ще немає
if [ ! -f /var/lib/postgresql/data/pg_hba.conf ]; then
    echo "# TYPE  DATABASE        USER            ADDRESS                 METHOD" > /var/lib/postgresql/data/pg_hba.conf
    echo "local   all            all                                     trust" >> /var/lib/postgresql/data/pg_hba.conf
    echo "host    all            all             127.0.0.1/32           md5" >> /var/lib/postgresql/data/pg_hba.conf
    echo "host    all            all             ::1/128                 md5" >> /var/lib/postgresql/data/pg_hba.conf
    echo "host    all            all             0.0.0.0/0              md5" >> /var/lib/postgresql/data/pg_hba.conf
    echo "host    all            all             192.168.193.0/24       md5" >> /var/lib/postgresql/data/pg_hba.conf
fi

# Запускаємо оригінальний entrypoint
exec docker-entrypoint.sh "$@" 