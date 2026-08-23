"""
Data models and dictionaries for Gesture recognition
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class GestureData:
    name: str
    symbol: str
    meaning: str
    category: str  # E.g. 'Буква', 'Команда', 'Экстренное'
    description: str


# Standard Sign Language gesture mappings
GESTURE_DICTIONARY: Dict[str, GestureData] = {
    "open_palm": GestureData(
        name="Открытая ладонь",
        symbol="✋",
        meaning="Привет / Стоп",
        category="Команда",
        description="Все пальцы выпрямлены и разведены."
    ),
    "thumbs_up": GestureData(
        name="Большой палец вверх",
        symbol="👍",
        meaning="Да / Хорошо",
        category="Команда",
        description="Большой палец выпрямлен вверх, остальные сжаты."
    ),
    "thumbs_down": GestureData(
        name="Большой палец вниз",
        symbol="👎",
        meaning="Нет / Плохо",
        category="Команда",
        description="Большой палец направлен вниз."
    ),
    "peace": GestureData(
        name="Знак победы (V)",
        symbol="✌️",
        meaning="Мир / Буква V / 2",
        category="Буква",
        description="Указательный и средний пальцы подняты в форме V."
    ),
    "fist": GestureData(
        name="Кулак",
        symbol="✊",
        meaning="Да / Помощь",
        category="Команда",
        description="Все пальцы плотно сжаты в кулак."
    ),
    "ok": GestureData(
        name="Знак OK",
        symbol="👌",
        meaning="Понятно / Отлично",
        category="Команда",
        description="Большой и указательный пальцы образуют кольцо."
    ),
    "sos_palm": GestureData(
        name="Сигнал SOS",
        symbol="🆘",
        meaning="Срочно нужна помощь!",
        category="Экстренное",
        description="Сжатие большого пальца в ладони с покрытием четырьмя пальцами."
    )
}
