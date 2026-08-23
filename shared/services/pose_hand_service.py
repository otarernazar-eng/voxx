"""
===============================================================================
VoxX - MediaPipe Pose & Hand Detection Service (Модуль 3)
Сервис захвата ключевых точек рук и тела, нормализации координат,
кольцевой буферизации (30-45 кадров) и отрисовки цветовых рамок обратной связи.
===============================================================================
"""
import json
import logging
import time
from collections import deque
from typing import Dict, List, Optional, Tuple, Any

import cv2
import numpy as np

# MediaPipe safety import
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

logger = logging.getLogger("PoseHandService")


def normalize_landmarks(
    landmarks: List[Dict[str, float]],
    image_width: int,
    image_height: int,
    is_front_camera: bool = True
) -> List[Dict[str, float]]:
    """
    Промпт 3.3 — Нормализация координат:
    Приводит координаты x, y к диапазону [0, 1] и корректно зеркалирует 
    координаты по оси X для фронтальной камеры (x_norm = 1.0 - x_norm).
    """
    normalized = []
    w = max(image_width, 1)
    h = max(image_height, 1)

    for lm in landmarks:
        raw_x = lm.get("x", 0.0)
        raw_y = lm.get("y", 0.0)
        raw_z = lm.get("z", 0.0)
        visibility = lm.get("visibility", 1.0)

        # Приведение к [0.0, 1.0] если координаты переданы в пикселях
        x_norm = raw_x if 0.0 <= raw_x <= 1.0 else raw_x / w
        y_norm = raw_y if 0.0 <= raw_y <= 1.0 else raw_y / h

        # Ограничение диапазона [0.0, 1.0]
        x_norm = float(np.clip(x_norm, 0.0, 1.0))
        y_norm = float(np.clip(y_norm, 0.0, 1.0))

        # Зеркалирование по горизонтали для фронтальной камеры
        if is_front_camera:
            x_norm = round(1.0 - x_norm, 4)
        else:
            x_norm = round(x_norm, 4)

        normalized.append({
            "x": x_norm,
            "y": round(y_norm, 4),
            "z": round(float(raw_z), 4),
            "visibility": round(float(visibility), 4)
        })

    return normalized


class LandmarkBuffer:
    """
    Промпт 3.4 — Кольцевой буфер последних 30-45 кадров:
    Хранит последние N кадров (по умолчанию 30). При заполнении старые кадры удаляются.
    """
    def __init__(self, capacity: int = 30):
        self.capacity = capacity
        self._buffer = deque(maxlen=capacity)

    def add(self, item: Dict[str, Any]) -> None:
        """Добавить новый кадр с точками в буфер."""
        self._buffer.append({
            "timestamp": time.time(),
            "data": item
        })

    def get_all(self) -> List[Dict[str, Any]]:
        """Получить все кадры в буфере."""
        return list(self._buffer)

    def clear(self) -> None:
        """Очистить буфер."""
        self._buffer.clear()

    @property
    def current_size(self) -> int:
        """Текущее количество кадров в буфере."""
        return len(self._buffer)

    def get_average_confidence(self) -> float:
        """Вычислить среднее значение уверенности распознавания по буферу."""
        if not self._buffer:
            return 0.0
        confidences = [item["data"].get("confidence", 0.0) for item in self._buffer]
        return float(np.mean(confidences))


class PoseHandService:
    """
    Промпт 3.1 — Сервис подключения MediaPipe Hands + Pose
    """
    def __init__(self, max_hands: int = 2, buffer_capacity: int = 30):
        self.max_hands = max_hands
        self.buffer = LandmarkBuffer(capacity=buffer_capacity)
        self.is_recording = False
        self.recorded_sequence: List[Dict[str, Any]] = []

        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_hands = mp.solutions.hands
                self.mp_pose = mp.solutions.pose
                self.mp_drawing = mp.solutions.drawing_utils

                self.hands_detector = self.mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=max_hands,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                self.pose_detector = self.mp_pose.Pose(
                    static_image_mode=False,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                self.models_loaded = True
            except Exception as e:
                logger.error(f"Ошибка загрузки MediaPipe моделей: {e}")
                self.models_loaded = False
        else:
            self.models_loaded = False

    def start_recording(self) -> None:
        """Промпт 3.2: Начать запись последовательности кадров."""
        self.is_recording = True
        self.recorded_sequence.clear()
        logger.info("Запись последовательности жестов начата.")

    def stop_recording(self) -> str:
        """Промпт 3.2: Остановить запись и вернуть JSON последовательности."""
        self.is_recording = False
        sequence_data = {
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_frames": len(self.recorded_sequence),
            "sequence": self.recorded_sequence
        }
        json_output = json.dumps(sequence_data, indent=2, ensure_ascii=False)
        logger.info(f"Запись завершена. Записано кадров: {len(self.recorded_sequence)}")
        return json_output

    def process_frame(
        self,
        frame_bgr: np.ndarray,
        is_front_camera: bool = True
    ) -> Dict[str, Any]:
        """
        Главный метод обработки кадра (Промпт 3.1 & 3.5):
        Возвращает словарь с ключевыми точками рук, позы, коэффициентом уверенности
        и аннотированным кадром с цветными рамками обратной связи.
        """
        default_result = {
            "hands": [],
            "pose": [],
            "confidence": 0.0,
            "status_text": "Не видно",
            "annotated_frame": frame_bgr,
            "rectangles": []
        }

        if frame_bgr is None or not self.models_loaded:
            return default_result

        h, w, c = frame_bgr.shape
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        annotated_frame = frame_bgr.copy()

        detected_hands = []
        pose_landmarks = []
        overall_confidence = 0.0
        status_text = "Не видно"

        try:
            # 1. Запуск MediaPipe Hands
            hands_res = self.hands_detector.process(rgb)

            if hands_res.multi_hand_landmarks:
                for idx, hand_lms in enumerate(hands_res.multi_hand_landmarks):
                    # Извлечение 21 точки руки
                    raw_lms = [{"x": lm.x, "y": lm.y, "z": lm.z, "visibility": getattr(lm, "visibility", 1.0)} for lm in hand_lms.landmark]
                    norm_lms = normalize_landmarks(raw_lms, w, h, is_front_camera)
                    detected_hands.append(norm_lms)

                    # Расчет Bounding Box для руки
                    xs = [int(lm.x * w) for lm in hand_lms.landmark]
                    ys = [int(lm.y * h) for lm in hand_lms.landmark]
                    x_min, x_max = max(0, min(xs) - 20), min(w, max(xs) + 20)
                    y_min, y_max = max(0, min(ys) - 20), min(h, max(ys) + 20)

                    # Оценка уверенности по размеру и видимости
                    hand_score = float(hands_res.multi_handedness[idx].classification[0].score) if hands_res.multi_handedness else 0.8
                    overall_confidence = max(overall_confidence, hand_score)

                    # =========================================================
                    # Промпт 3.5 — Визуальная обратная связь (Цветовые рамки)
                    # =========================================================
                    if hand_score > 0.7 and (x_max - x_min) > 40:
                        box_color = (0, 184, 0)      # Зеленая #00B894 (BGR)
                        status_text = "Хорошо видно"
                    elif hand_score >= 0.3:
                        box_color = (0, 215, 255)    # Желтая #FFD700 (BGR)
                        status_text = "Поднесите ближе"
                    else:
                        box_color = (117, 118, 255)  # Красная #FF7675 (BGR)
                        status_text = "Рука потеряна"

                    # Отрисовка прямоугольника и текста состояния на кадре
                    cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), box_color, 4)
                    cv2.putText(
                        annotated_frame,
                        f"{status_text} ({int(hand_score * 100)}%)",
                        (x_min, max(y_min - 10, 25)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        box_color,
                        2
                    )

                    # Отрисовка скелета руки через MediaPipe
                    self.mp_drawing.draw_landmarks(
                        annotated_frame,
                        hand_lms,
                        self.mp_hands.HAND_CONNECTIONS
                    )

            else:
                # Руки не обнаружены -> Красный статус
                status_text = "Не видно"
                cv2.putText(
                    annotated_frame,
                    "Рука потеряна",
                    (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (117, 118, 255),
                    3
                )

            # 2. Запуск MediaPipe Pose (33 точки позы)
            pose_res = self.pose_detector.process(rgb)
            if pose_res.pose_landmarks:
                raw_pose_lms = [{"x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility} for lm in pose_res.pose_landmarks.landmark]
                pose_landmarks = normalize_landmarks(raw_pose_lms, w, h, is_front_camera)

        except Exception as err:
            logger.warning(f"Сбой выполнения MediaPipe: {err}")

        # Формирование итогового результата
        result_data = {
            "hands": detected_hands,
            "pose": pose_landmarks,
            "confidence": overall_confidence,
            "status_text": status_text,
            "annotated_frame": annotated_frame
        }

        # Промпт 3.4 — Добавление кадра в кольцевой буфер
        self.buffer.add(result_data)

        # Промпт 3.2 — Фиксация в последовательности при активной записи
        if self.is_recording:
            self.recorded_sequence.append({
                "timestamp": time.time(),
                "confidence": overall_confidence,
                "hands_count": len(detected_hands),
                "hands_landmarks": detected_hands
            })

        return result_data
