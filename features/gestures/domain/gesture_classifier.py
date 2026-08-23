"""
===============================================================================
VoxX - Gesture Classifier Module (Модуль 4.1)
Интерфейс классификации и эвристический классификатор 5 статических + 1 динамического жеста.
===============================================================================
"""
from abc import ABC, abstractmethod
import math
import time
from typing import Dict, List, Optional, Tuple, Any


class IGestureClassifier(ABC):
    """
    Абстрактный интерфейс для классификаторов жестов.
    Позволяет легко заменить эвристический алгоритм на ML-модель (PyTorch/ONNX) в будущем.
    """
    @abstractmethod
    def classify(self, landmark_sequence: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Классифицирует последовательность кадров с ключевыми точками рук.
        Returns: Dict с полями 'gesture_id', 'name', 'confidence', 'type' или None.
        """
        pass


class RuleBasedGestureClassifier(IGestureClassifier):
    """
    Реализация классификатора жестов на геометрических правилах MediaPipe Hands.
    Поддерживает:
    - Статические жесты: "open_palm" (Привет), "fist" (Да), "pointing" (Указать), "thumbs_up" (Отлично), "ok" (Понятно).
    - Динамический жест: "waving" (Махание ладонью).
    """

    def _is_finger_extended(self, landmarks: List[Dict[str, float]], tip_idx: int, pip_idx: int) -> bool:
        """Проверяет, выпрямлен ли палец (расстояние от запястья 0 до кончика > до фаланги)."""
        wrist = landmarks[0]
        tip = landmarks[tip_idx]
        pip = landmarks[pip_idx]
        
        dist_tip = math.hypot(tip["x"] - wrist["x"], tip["y"] - wrist["y"])
        dist_pip = math.hypot(pip["x"] - wrist["x"], pip["y"] - wrist["y"])
        return dist_tip > dist_pip

    def classify_static_frame(self, hand_landmarks: List[Dict[str, float]]) -> Optional[Dict[str, Any]]:
        """
        Промпт 4.1 — Классификация единичного кадра статического жеста.
        MediaPipe landmark indices:
        - 0: Wrist
        - Thumb: 2 (MCP), 4 (TIP)
        - Index: 6 (PIP), 8 (TIP)
        - Middle: 10 (PIP), 12 (TIP)
        - Ring: 14 (PIP), 16 (TIP)
        - Pinky: 18 (PIP), 20 (TIP)
        """
        if not hand_landmarks or len(hand_landmarks) < 21:
            return None

        # Определение состояния пальцев
        thumb_extended = self._is_finger_extended(hand_landmarks, 4, 2)
        index_extended = self._is_finger_extended(hand_landmarks, 8, 6)
        middle_extended = self._is_finger_extended(hand_landmarks, 12, 10)
        ring_extended = self._is_finger_extended(hand_landmarks, 16, 14)
        pinky_extended = self._is_finger_extended(hand_landmarks, 20, 18)

        extended_count = sum([index_extended, middle_extended, ring_extended, pinky_extended])

        # 1. Открытая ладонь (Привет / Стоп) — Все 5 пальцев выпрямлены
        if thumb_extended and extended_count == 4:
            return {
                "gesture_id": "open_palm",
                "name": "Привет / Открытая ладонь",
                "symbol": "✋",
                "confidence": 0.95,
                "category": "статический"
            }

        # 2. Кулак (Да / Подтверждаю) — Все пальцы согнуты
        if not thumb_extended and extended_count == 0:
            return {
                "gesture_id": "fist",
                "name": "Да / Кулак",
                "symbol": "✊",
                "confidence": 0.92,
                "category": "статический"
            }

        # 3. Большой палец вверх (Отлично / Хорошо)
        if thumb_extended and extended_count == 0 and hand_landmarks[4]["y"] < hand_landmarks[3]["y"]:
            return {
                "gesture_id": "thumbs_up",
                "name": "Отлично / Большой палец вверх",
                "symbol": "👍",
                "confidence": 0.94,
                "category": "статический"
            }

        # 4. Указательный палец (Внимание / Указать)
        if index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return {
                "gesture_id": "pointing",
                "name": "Указать / Внимание",
                "symbol": "☝️",
                "confidence": 0.90,
                "category": "статический"
            }

        # 5. Жест ОК (Понятно / Отлично) — Соприкосновение большого и указательного пальца
        dist_thumb_index = math.hypot(
            hand_landmarks[4]["x"] - hand_landmarks[8]["x"],
            hand_landmarks[4]["y"] - hand_landmarks[8]["y"]
        )
        if dist_thumb_index < 0.08 and middle_extended and ring_extended and pinky_extended:
            return {
                "gesture_id": "ok_sign",
                "name": "Понятно (ОК)",
                "symbol": "👌",
                "confidence": 0.88,
                "category": "статический"
            }

        return None

    def classify_dynamic_sequence(self, landmark_sequence: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Промпт 4.1 — Распознавание динамического жеста (Махание ладонью).
        Анализирует колебания X-координаты запястья или ладони за последние 10-20 кадров.
        """
        if len(landmark_sequence) < 8:
            return None

        # Извлечение X-координат запястья за последовательность
        x_positions = []
        for frame in landmark_sequence:
            data = frame.get("data", {})
            hands = data.get("hands", [])
            if hands and len(hands[0]) > 0:
                x_positions.append(hands[0][0]["x"])

        if len(x_positions) < 8:
            return None

        # Расчет количества смен направления движения (пиков и впадин)
        diffs = [x_positions[i+1] - x_positions[i] for i in range(len(x_positions)-1)]
        direction_changes = 0
        for i in range(len(diffs)-1):
            if (diffs[i] > 0.01 and diffs[i+1] < -0.01) or (diffs[i] < -0.01 and diffs[i+1] > 0.01):
                direction_changes += 1

        # Если 2 и более раз изменилось направление -> Махание
        if direction_changes >= 2:
            return {
                "gesture_id": "waving",
                "name": "Приветствие (Махание)",
                "symbol": "👋",
                "confidence": 0.87,
                "category": "динамический"
            }

        return None

    def classify(self, landmark_sequence: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Единый метод классификации: проверяет динамические жесты, а затем статические.
        """
        dynamic_res = self.classify_dynamic_sequence(landmark_sequence)
        if dynamic_res:
            return dynamic_res

        if landmark_sequence:
            last_frame = landmark_sequence[-1].get("data", {})
            hands = last_frame.get("hands", [])
            if hands:
                return self.classify_static_frame(hands[0])

        return None
