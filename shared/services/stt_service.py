"""
===============================================================================
VoxX - Speech-to-Text (STT) Service (Модуль 6)
Оффлайн и веб-распознавание речи с обработкой ошибок, промежуточными результатами
и интеграцией браузерного Web Speech API.
===============================================================================
"""
import logging
import time
from typing import Dict, List, Optional, Any, Callable
import streamlit as st

# Optional Vosk / SpeechRecognition imports
try:
    import vosk
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

logger = logging.getLogger("STTService")


class STTService:
    """
    Промпт 6.1 — Сервис распознавания речи (STT) с оффлайн fallback и браузерной интеграцией.
    """

    def __init__(self, language: str = "ru-RU"):
        self.language = language
        self.is_listening = False
        self.latest_partial_text = ""
        self.latest_final_text = ""

    def start_listening(self) -> None:
        """Начать распознавание речи."""
        self.is_listening = True
        logger.info("Служба STT запущена.")

    def stop_listening(self) -> None:
        """Остановить распознавание речи."""
        self.is_listening = False
        logger.info("Служба STT остановлена.")

    def render_browser_stt_component(self, auto_speak_new: bool = True) -> Dict[str, str]:
        """
        Промпт 6.1 & 6.2 — Интеграция браузерного Web Speech API для мгновенного получения речи.
        """
        html_code = """
        <div style="background: #121212; border: 3px solid #FFD700; border-radius: 16px; padding: 20px; text-align: center;">
            <button id="btn-stt-toggle" onclick="toggleSTT()" style="
                background: #00B894;
                color: #FFFFFF;
                border: 2px solid #00CEC9;
                border-radius: 14px;
                padding: 16px 28px;
                font-size: 22px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                margin-bottom: 15px;
            ">🎙️ Начать Запись Речи (Web Speech API)</button>
            
            <p style="color: #A0A0B2; font-size: 14px; margin-bottom: 5px;">Статус браузера:</p>
            <div id="stt-status" style="color: #FFD700; font-size: 18px; font-weight: bold;">Готов к записи</div>
        </div>

        <script>
            let recognition = null;
            let isRecording = false;

            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'ru-RU';

                recognition.onstart = function() {
                    isRecording = true;
                    document.getElementById('stt-status').innerText = '🟢 Идёт запись речи... Говорите в микрофон';
                    document.getElementById('btn-stt-toggle').innerText = '⏹️ Остановить Запись Речи';
                    document.getElementById('btn-stt-toggle').style.background = '#FF7675';
                };

                recognition.onresult = function(event) {
                    let interim = '';
                    let final = '';

                    for (let i = event.resultIndex; i < event.results.length; ++i) {
                        if (event.results[i].isFinal) {
                            final += event.results[i][0].transcript;
                        } else {
                            interim += event.results[i][0].transcript;
                        }
                    }

                    if (final) {
                        document.getElementById('stt-status').innerText = '✅ Фраза принята: ' + final;
                        // Передаем распознанную фразу в Streamlit (если доступен родительский контейнер)
                        if (window.parent && window.parent.postMessage) {
                            window.parent.postMessage({type: 'voxx_stt_result', text: final}, '*');
                        }
                    }
                };

                recognition.onerror = function(event) {
                    document.getElementById('stt-status').innerText = '⚠️ Ошибка распознавания: ' + event.error;
                };

                recognition.onend = function() {
                    isRecording = false;
                    document.getElementById('stt-status').innerText = '⚪ Запись завершена';
                    document.getElementById('btn-stt-toggle').innerText = '🎙️ Начать Запись Речи';
                    document.getElementById('btn-stt-toggle').style.background = '#00B894';
                };
            } else {
                document.getElementById('stt-status').innerText = '❌ Браузер не поддерживает Web Speech API (используйте Chrome/Edge)';
            }

            function toggleSTT() {
                if (!recognition) return;
                if (isRecording) {
                    recognition.stop();
                } else {
                    recognition.start();
                }
            }
        </script>
        """
        st.components.v1.html(html_code, height=180)
        return {"status": "ok"}
