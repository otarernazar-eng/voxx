"""
Vision & OCR Domain Logic Processor
Uses OpenCV preprocessing + pytesseract/Fallback image analyzer.
"""
from typing import Tuple, Dict, Any
import numpy as np
import cv2
from PIL import Image


class OCRObjectDetector:
    def __init__(self):
        self._tesseract_available = False
        self._try_init_tesseract()

    def _try_init_tesseract(self):
        try:
            import pytesseract
            self._tesseract_available = True
        except Exception:
            self._tesseract_available = False

    def extract_text_from_image(self, pil_image: Image.Image, lang: str = "rus+eng") -> str:
        """Extract text content from input image."""
        if pil_image is None:
            return ""

        if self._tesseract_available:
            try:
                import pytesseract
                text = pytesseract.image_to_string(pil_image, lang=lang)
                if text.strip():
                    return text.strip()
            except Exception:
                pass

        # Fallback smart scene description when pytesseract OCR engine binary is not installed locally
        return self._generate_heuristic_ocr_fallback(pil_image)

    def analyze_scene_accessibility(self, image_np: np.ndarray) -> Dict[str, Any]:
        """Calculate image brightness, contrast, and visual readability metrics."""
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        mean_brightness = float(np.mean(gray))
        std_contrast = float(np.std(gray))

        is_dark = mean_brightness < 80
        is_high_contrast = std_contrast > 50

        return {
            "brightness": round(mean_brightness, 1),
            "contrast": round(std_contrast, 1),
            "is_dark": is_dark,
            "is_high_contrast": is_high_contrast,
            "recommendation": "Рекомендуется включить дополнительное освещение" if is_dark else "Освещенность хорошая"
        }

    def _generate_heuristic_ocr_fallback(self, img: Image.Image) -> str:
        """Fallback description when Tesseract CLI binary is absent."""
        width, height = img.size
        return (
            f"Изображение загружено ({width}x{height} px). "
            f"Ассистент зрения готов озвучить содержимое. "
            f"Для работы офлайн-OCR убедитесь в установке tesseract-ocr."
        )
