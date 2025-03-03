from typing import Final

from aiogram.filters import Filter, StateFilter

# Фільтр, що відповідає відсутності стану (None)
# Використовується для обробки повідомлень, коли користувач не знаходиться в жодному стані
NoneState: Final[Filter] = StateFilter(None)

# Фільтр, що відповідає будь-якому стану, крім None
# Використовується для обробки повідомлень, коли користувач знаходиться в будь-якому стані
# Створюється як заперечення NoneState за допомогою оператора ~
AnyState: Final[Filter] = ~NoneState
