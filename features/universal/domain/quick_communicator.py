"""
AAC Quick Communication & Emergency Domain Model Manager
"""
from typing import List
from shared.models.phrase_model import AACPhrase


class QuickCommunicator:
    def __init__(self):
        self.default_phrases: List[AACPhrase] = [
            AACPhrase("p1", "Мне нужна помощь", "Базовые", "🆘", bg_color="#FF7675", is_emergency=True),
            AACPhrase("p2", "Спасибо!", "Базовые", "🙏", bg_color="#00B894"),
            AACPhrase("p3", "Да", "Базовые", "✅", bg_color="#0984E3"),
            AACPhrase("p4", "Нет", "Базовые", "❌", bg_color="#D63031"),
            AACPhrase("p5", "Где туалет?", "Навигация", "🚻", bg_color="#6C5CE7"),
            AACPhrase("p6", "Вызовите врача", "Здоровье", "🚑", bg_color="#D63031", is_emergency=True),
            AACPhrase("p7", "Я плохо слышу", "Инфо", "👂", bg_color="#FDCB6E"),
            AACPhrase("p8", "Повторите, пожалуйста", "Общение", "🔄", bg_color="#6C5CE7"),
            AACPhrase("p9", "Сколько это стоит?", "Покупки", "💳", bg_color="#00CEC9"),
            AACPhrase("p10", "Напишите на бумаге", "Общение", "📝", bg_color="#6C5CE7")
        ]

    def get_phrases_by_category(self, category: str = "Все") -> List[AACPhrase]:
        """Return phrases filtered by category."""
        if category == "Все":
            return self.default_phrases
        return [p for p in self.default_phrases if p.category == category]
