"""
VoxX System Configuration and Constants
"""
from dataclasses import dataclass
from typing import Dict, Any

APP_NAME = "VoxX"
APP_SLOGAN = "Доступная среда для каждого"
APP_VERSION = "1.0.0"
AUTHOR = "Senior Python/Streamlit Developer"

# Color Palette (Accessibility-Oriented)
class COLORS:
    PRIMARY = "#6C5CE7"           # Deep Purple / Indigo Accent
    PRIMARY_HOVER = "#5B4BC4"
    ACCENT = "#00CEC9"            # Vibrant Teal
    BACKGROUND_DARK = "#0F0F1A"    # Rich Dark BG
    SURFACE_CARD = "#1A1A2E"       # Glass/Card BG
    SURFACE_BORDER = "#2E2E4A"     # Card Border
    
    TEXT_PRIMARY = "#F1F1F6"      # High readability text
    TEXT_MUTED = "#A0A0B2"        # Subtitle / secondary text
    TEXT_INVERTED = "#0F0F1A"
    
    # Status Indicators
    SUCCESS = "#00B894"           # Mint Green
    WARNING = "#FDCB6E"           # Bright Amber
    ERROR = "#FF7675"             # Soft Coral Red
    INFO = "#0984E3"              # Electric Blue
    
    # High Contrast Mode Palette
    HC_BACKGROUND = "#000000"
    HC_SURFACE = "#121212"
    HC_BORDER = "#FFFF00"         # High contrast yellow border
    HC_TEXT = "#FFFFFF"
    HC_ACCENT = "#00FFFF"         # Cyan


@dataclass
class AccessibilityDefaults:
    FONT_SIZE_SCALE: float = 1.0  # 1.0 = Normal, 1.25 = Large, 1.5 = Extra Large
    HIGH_CONTRAST: bool = False
    READING_GUIDE: bool = False
    TTS_SPEED: int = 150          # Words per minute
    TTS_LANGUAGE: str = "ru"
    OFFLINE_STT: bool = True
    VIBRATION_FEEDBACK: bool = True


# Navigation Items Configuration
NAV_ITEMS: Dict[str, Dict[str, Any]] = {
    "home": {
        "title": "Главная",
        "icon": "🏠",
        "route": "pages/1_Home.py",
        "desc": "Обзор возможностей и быстрый доступ к инструментам доступности."
    },
    "gestures": {
        "title": "Жесты",
        "icon": "🤟",
        "route": "pages/2_Жесты.py",
        "desc": "Перевод жестового языка в текст и речь через камеру."
    },
    "hearing": {
        "title": "Слух",
        "icon": "👂",
        "route": "pages/3_Слух.py",
        "desc": "Распознавание речи в текст в реальном времени и визуализатор звуков."
    },
    "vision": {
        "title": "Зрение",
        "icon": "👁️",
        "route": "pages/4_Зрение.py",
        "desc": "Распознавание текста с фото/камеры (OCR) и голосовая озвучка (TTS)."
    },
    "universal": {
        "title": "Универсальный",
        "icon": "💬",
        "route": "pages/5_Универсальный.py",
        "desc": "Ассистент общения с быстрыми карточками фраз (AAC) и кнопкой SOS."
    },
    "settings": {
        "title": "Настройки",
        "icon": "⚙️",
        "route": "pages/6_Настройки.py",
        "desc": "Персонализация размера шрифта, контрастности и голосовых настроек."
    },
    "about": {
        "title": "О приложении",
        "icon": "ℹ️",
        "route": "pages/7_О_приложении.py",
        "desc": "Информация о VoxX, лицензия и диагностика системы."
    }
}
