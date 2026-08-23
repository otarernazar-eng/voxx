"""
===============================================================================
VoxX - RSL (РЖЯ) Gesture Dictionary (Модуль 4.2)
Словарь из 25 базовых жестов русского жестового языка с поиском.
===============================================================================
"""
from typing import Dict, List, Any

# 25 базовых жестов РЖЯ
GESTURE_DICTIONARY: List[Dict[str, Any]] = [
    {"id": "hello", "name": "Привет", "symbol": "👋", "category": "динамический", "description": "Махание открытой ладонью из стороны в сторону"},
    {"id": "thanks", "name": "Спасибо", "symbol": "🙏", "category": "статический", "description": "Прикладывание ладони к груди или подбородку"},
    {"id": "yes", "name": "Да", "symbol": "✊", "category": "статический", "description": "Сжатый кулак, естественный кивок вниз"},
    {"id": "no", "name": "Нет", "symbol": "✋", "category": "динамический", "description": "Качание указательного пальца из стороны в сторону"},
    {"id": "help", "name": "Помощь", "symbol": "🆘", "category": "статический", "description": "Открытая ладонь вверх с прижатой другой рукой"},
    {"id": "toilet", "name": "Туалет", "symbol": "🚾", "category": "статический", "description": "Жест буквой 'Т' пальцами руки"},
    {"id": "water", "name": "Вода / Пить", "symbol": "🚰", "category": "динамический", "description": "Поднесение сжатой кисти куполом к губам"},
    {"id": "price", "name": "Сколько стоит", "symbol": "💰", "category": "динамический", "description": "Потирание большого и указательного пальцев"},
    {"id": "not_hearing", "name": "Я не слышу", "symbol": "🔇", "category": "статический", "description": "Указательный палец к уху, затем качание в сторону"},
    {"id": "sorry", "name": "Извините", "symbol": "🤝", "category": "статический", "description": "Ладонь на груди с легким круговым движением"},
    {"id": "where", "name": "Где", "symbol": "❓", "category": "динамический", "description": "Разведенные в стороны ладони вверх"},
    {"id": "when", "name": "Когда", "symbol": "⏰", "category": "статический", "description": "Указание на запястье (часы)"},
    {"id": "good", "name": "Хорошо", "symbol": "👍", "category": "статический", "description": "Большой палец поднятый вверх"},
    {"id": "bad", "name": "Плохо", "symbol": "👎", "category": "статический", "description": "Большой палец опущенный вниз"},
    {"id": "doctor", "name": "Врач / Доктор", "symbol": "🩺", "category": "статический", "description": "Касание двух пальцев запястья (пульс)"},
    {"id": "hospital", "name": "Больница", "symbol": "🏥", "category": "статический", "description": "Изображение креста пальцем на плече"},
    {"id": "food", "name": "Еда / Кушать", "symbol": "🍽️", "category": "динамический", "description": "Сложенные вместе пальцы подносятся к рту"},
    {"id": "please", "name": "Пожалуйста", "symbol": "🤲", "category": "статический", "description": "Две открытые ладони, протянутые вперед"},
    {"id": "repeat", "name": "Повторите", "symbol": "🔄", "category": "динамический", "description": "Круговое движение указательным пальцем"},
    {"id": "understand", "name": "Понятно (ОК)", "symbol": "👌", "category": "статический", "description": "Кольцо из большого и указательного пальцев"},
    {"id": "family", "name": "Семья", "symbol": "👨‍👩‍👧", "category": "динамический", "description": "Соединение двух кистей руки в полукруг"},
    {"id": "home", "name": "Дом", "symbol": "🏠", "category": "статический", "description": "Кончики пальцев обеих рук образуют крышу"},
    {"id": "friend", "name": "Друг", "symbol": "🤝", "category": "статический", "description": "Пожатие собственных рук ладонями"},
    {"id": "goodbye", "name": "До свидания", "symbol": "👋", "category": "динамический", "description": "Сгибание пальцев открытой ладони"},
    {"id": "danger", "name": "Опасность / SOS", "symbol": "🚨", "category": "динамический", "description": "Быстрые взмахи двумя руками над головой"}
]


def search_gestures(query: str) -> List[Dict[str, Any]]:
    """
    Промпт 4.2 — Простой поиск жестов РЖЯ по названию или описанию.
    """
    if not query or not query.strip():
        return GESTURE_DICTIONARY

    q = query.strip().lower()
    results = []

    for item in GESTURE_DICTIONARY:
        if q in item["name"].lower() or q in item["description"].lower() or q in item["category"].lower():
            results.append(item)

    return results
