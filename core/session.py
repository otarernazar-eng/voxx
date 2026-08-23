"""
VoxX Session State Management
Centralized state initialization and state helper functions for Streamlit.
"""
import time
import streamlit as st
from core.config import AccessibilityDefaults, APP_NAME


def init_session_state():
    """Ensure all required session state variables exist with safe default values."""
    defaults = {
        "app_initialized": True,
        "app_name": APP_NAME,
        "active_mode": "home",
        "current_mode": "Главная",
        "permissions_prompt_dismissed": False,
        
        # Accessibility Settings
        "font_size_scale": 1.0,           # Slider 1.0 to 2.0
        "high_contrast": True,             # Default ON
        "screenreader_mode": False,        # Simplified interface toggle for screen readers
        "tts_speed_rate": 1.0,            # Speech rate slider 0.5 to 2.0
        "tts_speed": 150,                 # Legacy words per min
        "tts_pitch": 1.0,                 # Pitch slider 0.5 to 2.0
        "tts_language": "ru-RU",
        "stt_language": "ru-RU",
        "offline_stt": True,
        "vibration_feedback": True,
        "reading_guide": False,
        
        # Features History State
        "gesture_history": [],
        "last_detected_gesture": "Ожидание...",
        "gesture_confidence": 0.0,
        "stt_transcript_history": [],
        "current_stt_text": "",
        "ocr_result_text": "",
        "last_spoken_phrase": "",
        "emergency_sos_active": False,
        "custom_quick_phrases": [
            "Мне нужна помощь",
            "Где находится туалет?",
            "Вызовите врача",
            "Я плохо слышу",
            "Повторите, пожалуйста",
            "Спасибо!",
            "Да",
            "Нет"
        ]
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def add_gesture_to_history(gesture_name: str, confidence: float = 0.0) -> None:
    """Record detected gesture into session history list."""
    if "gesture_history" not in st.session_state:
        st.session_state["gesture_history"] = []
    
    st.session_state["last_detected_gesture"] = gesture_name
    st.session_state["gesture_confidence"] = confidence
    
    st.session_state["gesture_history"].append({
        "name": gesture_name,
        "confidence": confidence,
        "timestamp": time.time()
    })
    # Keep last 50 items
    if len(st.session_state["gesture_history"]) > 50:
        st.session_state["gesture_history"] = st.session_state["gesture_history"][-50:]


def reset_accessibility_settings():
    """Reset all accessibility sliders and toggles to default high-contrast values."""
    st.session_state.font_size_scale = 1.0
    st.session_state.high_contrast = True
    st.session_state.screenreader_mode = False
    st.session_state.tts_speed_rate = 1.0
    st.session_state.tts_speed = 150
    st.session_state.tts_pitch = 1.0
    st.session_state.vibration_feedback = True
    st.session_state.reading_guide = False
