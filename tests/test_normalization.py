"""
Unit Tests for Landmark Normalization & LandmarkBuffer (Модуль 3)
"""
import unittest
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from voxx.shared.services.pose_hand_service import normalize_landmarks, LandmarkBuffer


class TestLandmarkNormalization(unittest.TestCase):

    def test_normalize_landmarks_range(self):
        """Проверка приведения пиксельных координат к диапазону [0.0, 1.0]"""
        raw_lms = [
            {"x": 320, "y": 240, "z": 0.5, "visibility": 0.9},
            {"x": 640, "y": 480, "z": 0.1, "visibility": 1.0}
        ]
        norm = normalize_landmarks(raw_lms, image_width=640, image_height=480, is_front_camera=False)
        
        self.assertEqual(len(norm), 2)
        self.assertEqual(norm[0]["x"], 0.5)
        self.assertEqual(norm[0]["y"], 0.5)
        self.assertEqual(norm[1]["x"], 1.0)
        self.assertEqual(norm[1]["y"], 1.0)

    def test_front_camera_mirroring(self):
        """Проверка зеркалирования по горизонтали для фронтальной камеры (1.0 - x)"""
        raw_lms = [{"x": 0.2, "y": 0.4, "z": 0.0, "visibility": 1.0}]
        
        # Front camera = True
        norm_front = normalize_landmarks(raw_lms, image_width=100, image_height=100, is_front_camera=True)
        self.assertAlmostEqual(norm_front[0]["x"], 0.8, places=2)

        # Front camera = False
        norm_rear = normalize_landmarks(raw_lms, image_width=100, image_height=100, is_front_camera=False)
        self.assertAlmostEqual(norm_rear[0]["x"], 0.2, places=2)


class TestLandmarkBuffer(unittest.TestCase):

    def test_buffer_capacity(self):
        """Проверка кольцевого буфера и удаления старых элементов при превышении емкости"""
        buffer = LandmarkBuffer(capacity=5)
        
        for i in range(10):
            buffer.add({"frame_index": i, "confidence": 0.8})

        self.assertEqual(buffer.current_size, 5)
        all_items = buffer.get_all()
        # Должны остаться последние 5 элементов (индексы 5..9)
        first_item_index = all_items[0]["data"]["frame_index"]
        self.assertEqual(first_item_index, 5)


if __name__ == "__main__":
    unittest.main()
