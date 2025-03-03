from enum import StrEnum, auto


class MiddlewareEventType(StrEnum):
    """
    Перелік типів подій, які можуть бути оброблені middleware в Telegram боті.
    
    Цей перелік визначає всі можливі типи оновлень, які можуть надходити
    від Telegram API та оброблятися middleware. Використовується для
    ідентифікації типу події в обробниках та middleware.
    
    Успадковує StrEnum, що дозволяє використовувати рядкові значення
    для елементів перерахування замість числових.
    """
    
    # Основні типи оновлень
    UPDATE = auto()  # Загальний тип для будь-якого оновлення
    
    # Типи повідомлень
    MESSAGE = auto()  # Звичайне повідомлення
    EDITED_MESSAGE = auto()  # Відредаговане повідомлення
    CHANNEL_POST = auto()  # Повідомлення в каналі
    EDITED_CHANNEL_POST = auto()  # Відредаговане повідомлення в каналі
    
    # Бізнес-повідомлення
    BUSINESS_CONNECTION = auto()  # Підключення до бізнес-акаунту
    BUSINESS_MESSAGE = auto()  # Бізнес-повідомлення
    EDITED_BUSINESS_MESSAGE = auto()  # Відредаговане бізнес-повідомлення
    DELETED_BUSINESS_MESSAGES = auto()  # Видалені бізнес-повідомлення
    
    # Реакції на повідомлення
    MESSAGE_REACTION = auto()  # Реакція на повідомлення
    MESSAGE_REACTION_COUNT = auto()  # Кількість реакцій на повідомлення
    
    # Інлайн-запити
    INLINE_QUERY = auto()  # Інлайн-запит
    CHOSEN_INLINE_RESULT = auto()  # Вибраний результат інлайн-запиту
    
    # Callback-запити та платежі
    CALLBACK_QUERY = auto()  # Callback-запит від інлайн-кнопок
    SHIPPING_QUERY = auto()  # Запит на доставку (платежі)
    PRE_CHECKOUT_QUERY = auto()  # Запит перед оплатою
    PURCHASED_PAID_MEDIA = auto()  # Придбаний платний контент
    
    # Опитування
    POLL = auto()  # Опитування
    POLL_ANSWER = auto()  # Відповідь на опитування
    
    # Зміни в чатах
    MY_CHAT_MEMBER = auto()  # Зміна статусу бота в чаті
    CHAT_MEMBER = auto()  # Зміна статусу учасника чату
    CHAT_JOIN_REQUEST = auto()  # Запит на приєднання до чату
    CHAT_BOOST = auto()  # Бустинг чату
    REMOVED_CHAT_BOOST = auto()  # Видалений буст чату
    
    # Помилки
    ERROR = auto()  # Помилка обробки оновлення
