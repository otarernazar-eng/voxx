"""
Sound Classification & Ambient Noise Monitoring Domain Logic
"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class SoundEvent:
    name: str
    icon: str
    decibels: float
    alert_level: str  # Normal, Warning, Critical
    recommendation: str


class SoundClassifier:
    def __init__(self):
        self.known_sounds: Dict[str, SoundEvent] = {
            "siren": SoundEvent("Сигнал тревоги / Сирена", "🚨", 85.0, "Critical", "Срочно обратите внимание! Опасность."),
            "doorbell": SoundEvent("Дверной звонок", "🔔", 65.0, "Warning", "Кто-то звонит в дверь."),
            "knock": SoundEvent("Стук в дверь", "✊", 60.0, "Warning", "Стук возле вашей двери."),
            "baby_cry": SoundEvent("Плач ребенка", "👶", 70.0, "Warning", "Малышу требуется внимание."),
            "speech": SoundEvent("Разговорная речь", "🗣️", 55.0, "Normal", "Обычный уровень шума речи.")
        }

    def evaluate_noise_level(self, db: float) -> str:
        """Categorize noise level in dB."""
        if db >= 80.0:
            return "Critical"
        elif db >= 60.0:
            return "Warning"
        return "Normal"
