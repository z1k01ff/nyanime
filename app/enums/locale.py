from __future__ import annotations

from enum import StrEnum, auto


class Locale(StrEnum):
    """
    Перелік підтримуваних мов локалізації.
    
    Цей клас визначає всі мови, які підтримуються ботом для локалізації.
    Кожен елемент представляє код мови відповідно до стандарту ISO 639-1.
    """
    EN = auto()  # English
    UK = auto()  # Ukrainian
    AR = auto()  # Arabic
    AZ = auto()  # Azerbaijani
    BE = auto()  # Belarusian
    CS = auto()  # Czech
    DE = auto()  # German
    ES = auto()  # Spanish
    FA = auto()  # Persian
    FR = auto()  # French
    HE = auto()  # Hebrew
    HI = auto()  # Hindi
    ID = auto()  # Indonesian
    IT = auto()  # Italian
    JA = auto()  # Japanese
    KK = auto()  # Kazakh
    KO = auto()  # Korean
    MS = auto()  # Malay
    NL = auto()  # Dutch
    PL = auto()  # Polish
    PT = auto()  # Portuguese
    RO = auto()  # Romanian
    SR = auto()  # Serbian
    TR = auto()  # Turkish
    UZ = auto()  # Uzbek
    VI = auto()  # Vietnamese
    RU = auto()  # Russian
