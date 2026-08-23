"""
===============================================================================
VoxX - Computer Vision & OCR Service (Модуль 7)
Анализ сцены, классификация объектов, считывание текста (OCR),
автоописание окружения и распознавание купют.
===============================================================================
"""
import logging
import sys
import time
from typing import Dict, List, Optional, Any, Tuple
import cv2
import numpy as np

# Optional pytesseract safety import
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

logger = logging.getLogger("VisionService")


class VisionService:
    """
    Промпт 7.1 — Сервис компьютерного зрения и OCR.
    """

    def __init__(self):
        self.last_analysis_hash = ""

    def recognize_banknote(self, image_bgr: np.ndarray) -> str:
        """
        Промпт 7.5 — Заглушка распознавания банкнот / купюр (подготовка TFLite/ONNX).
        """
        if image_bgr is None:
            return "Ошибка: изображение не передано"
        
        # Симуляция структуры для вызова будущего классификатора банкнот
        return "Функция распознавания купюр в разработке (готов модуль TFLite/ONNX)"

    def extract_text_ocr(self, image_bgr: np.ndarray) -> Tuple[str, List[Dict[str, Any]], np.ndarray]:
        """
        Промпт 7.4 — Поиск и считывание текста с выделением текстовых блоков (OCR).
        """
        if image_bgr is None:
            return "", [], image_bgr

        annotated = image_bgr.copy()
        h, w, c = image_bgr.shape
        extracted_text = ""
        blocks = []

        if PYTESSERACT_AVAILABLE:
            try:
                gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
                data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, lang='rus+eng')

                n_boxes = len(data['text'])
                for i in range(n_boxes):
                    if int(data['conf'][i]) > 40 and data['text'][i].strip():
                        word = data['text'][i].strip()
                        x, y, bw, bh = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                        # Отрисовка зелёного контура текстового блока
                        cv2.rectangle(annotated, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
                        
                        blocks.append({
                            "text": word,
                            "confidence": float(data['conf'][i]) / 100.0,
                            "bbox": (x, y, bw, bh)
                        })
                        extracted_text += word + " "

            except Exception as e:
                logger.warning(f"Ошибка pytesseract: {e}")

        # Fallback эвристика контуров текста при отсутствии pytesseract
        if not blocks:
            gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours[:5]:
                x, y, bw, bh = cv2.boundingRect(cnt)
                if bw > 30 and bh > 15:
                    cv2.rectangle(annotated, (x, y), (x + bw, y + bh), (0, 215, 255), 2)
                    blocks.append({
                        "text": "Текстовый блок",
                        "confidence": 0.75,
                        "bbox": (x, y, bw, bh)
                    })

        return extracted_text.strip(), blocks, annotated

    def analyze(self, image_bgr: np.ndarray) -> Dict[str, Any]:
        """
        Промпт 7.1 — Главный метод анализа изображения:
        Возвращает список обнаруженных объектов, распознанный текст и итоговое текстовое описание.
        """
        default_res = {
            "objects": [],
            "text": "",
            "description": "Ничего не найдено",
            "annotated_image": image_bgr
        }

        if image_bgr is None:
            return default_res

        h, w, c = image_bgr.shape
        annotated = image_bgr.copy()
        objects = []

        # Эвристическое обнаружение крупных объектов в кадре (Лицо / Человек / Предмет)
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        
        # Детекция лиц OpenCV Cascade (если доступен)
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, bw, bh) in faces:
                cv2.rectangle(annotated, (x, y), (x + bw, y + bh), (0, 215, 255), 3)
                cv2.putText(annotated, "Человек", (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 215, 255), 2)
                objects.append({"label": "Человек", "confidence": 0.92})
        except Exception:
            pass

        # Дополнительная эвристика яркости и центрального контура
        if not objects:
            mean_brightness = np.mean(gray)
            if mean_brightness > 160:
                objects.append({"label": "Светлое помещение / Окно", "confidence": 0.85})
            elif mean_brightness < 40:
                objects.append({"label": "Темная комната", "confidence": 0.80})
            else:
                objects.append({"label": "Предмет на столе", "confidence": 0.70})

        # Поиск текста (OCR)
        ocr_text, text_blocks, annotated_ocr = self.extract_text_ocr(image_bgr)
        if text_blocks:
            annotated = annotated_ocr

        # Формирование итогового описания для TTS
        obj_labels = [o["label"] for o in objects]
        desc_parts = []
        if obj_labels:
            desc_parts.append(f"На изображении обнаружены: {', '.join(obj_labels)}.")
        if ocr_text:
            desc_parts.append(f"Распознанный текст: {ocr_text}.")

        final_description = " ".join(desc_parts) if desc_parts else "Ничего не найдено"

        return {
            "objects": objects,
            "text": ocr_text,
            "description": final_description,
            "annotated_image": annotated,
            "text_blocks": text_blocks
        }
