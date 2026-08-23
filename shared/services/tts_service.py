"""
===============================================================================
VoxX - Text-to-Speech (TTS) Service (Модуль 5)
Оффлайн синтез речи с поддержкой pyttsx3, очереди фраз (до 10), 
Web Speech API fallback и сохранением последней произнесенной фразы.
===============================================================================
"""
from collections import deque
import logging
import sys
from typing import Dict, List, Optional, Any
import streamlit as st

# Optional pyttsx3 safety import
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except Exception:
    PYTTSX3_AVAILABLE = False

logger = logging.getLogger("TTSService")


class TTSService:
    """
    Промпт 5.1 & 5.4 — Сервис синтеза речи с очередью и fallback-логикой.
    """

    def __init__(self, max_queue_size: int = 10):
        self.max_queue_size = max_queue_size
        self.speech_queue = deque(maxlen=max_queue_size)
        self.rate = 1.0
        self.pitch = 1.0
        self.volume = 1.0
        self.engine = None

        if PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 150)
                self.engine.setProperty("volume", 1.0)
            except Exception as err:
                logger.warning(f"Сбой инициализации pyttsx3: {err}")
                self.engine = None

    def get_available_voices(self) -> List[Dict[str, str]]:
        """Возвращает список доступных системных голосов."""
        voices_list = [
            {"id": "ru-RU-female", "name": "Русский (Женский - Web Speech)"},
            {"id": "ru-RU-male", "name": "Русский (Мужской - Web Speech)"}
        ]

        if self.engine:
            try:
                py_voices = self.engine.getProperty("voices")
                for v in py_voices:
                    voices_list.append({
                        "id": v.id,
                        "name": getattr(v, "name", v.id)
                    })
            except Exception:
                pass

        return voices_list

    def set_rate(self, rate: float) -> None:
        """Настройка скорости речи (0.5 до 2.0)."""
        self.rate = max(0.5, min(2.0, rate))
        if self.engine:
            try:
                self.engine.setProperty("rate", int(150 * self.rate))
            except Exception:
                pass

    def set_pitch(self, pitch: float) -> None:
        """Настройка высоты тона (0.5 до 2.0)."""
        self.pitch = max(0.5, min(2.0, pitch))

    def set_volume(self, volume: float) -> None:
        """Настройка громкости (0.0 до 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.engine:
            try:
                self.engine.setProperty("volume", self.volume)
            except Exception:
                pass

    def stop(self) -> None:
        """Промпт 5.4: Очистить очередь речи и остановить озвучивание."""
        self.speech_queue.clear()
        if self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass
        
        # Браузерный стоп через HTML/JS
        st.components.v1.html(
            """
            <script>
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                }
            </script>
            """,
            height=0
        )
        logger.info("Очередь речи очищена, озвучка остановлена.")

    def get_queue_length(self) -> int:
        """Промпт 5.4: Возвращает длину текущей очереди фраз."""
        return len(self.speech_queue)

    def speak(self, text: str, force_browser: bool = True) -> None:
        """
        Промпт 5.1 & 5.4: Добавить фразу в очередь и воспроизвести голосом.
        """
        if not text or not text.strip():
            return

        clean_text = text.strip()
        
        # Добавление в очередь
        self.speech_queue.append(clean_text)

        # Сохранение последней произнесенной фразы в session_state (Промпт 5.5)
        if "last_spoken_phrase" in st.session_state:
            st.session_state["last_spoken_phrase"] = clean_text

        # 1. Попытка озвучки через pyttsx3
        if self.engine and not force_browser:
            try:
                self.engine.say(clean_text)
                self.engine.runAndWait()
                return
            except Exception as e:
                logger.warning(f"pyttsx3 error: {e}")

        # 2. Браузерный Web Speech API fallback (JS SpeechSynthesis)
        js_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel(); // Сброс старой речи
                const utterance = new SpeechSynthesisUtterance({json_escape_string(clean_text)});
                utterance.lang = 'ru-RU';
                utterance.rate = {self.rate};
                utterance.pitch = {self.pitch};
                utterance.volume = {self.volume};
                window.speechSynthesis.speak(utterance);
            }}
        </script>
        """
        st.components.v1.html(js_code, height=0)


def json_escape_string(text: str) -> str:
    """Безопасное экранирование строки для JS."""
    escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    return f'"{escaped}"'
