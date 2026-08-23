"""
VoxX Helper Utilities
Image handling, audio encoding, HTML synthesis wrappers, formatting.
"""
import base64
import io
import time
from typing import Optional
from PIL import Image
import numpy as np
import streamlit as st


def pil_to_bytes(image: Image.Image, format_type: str = "PNG") -> bytes:
    """Convert PIL Image to bytes."""
    buf = io.BytesIO()
    image.save(buf, format=format_type)
    return buf.getvalue()


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to Base64 string for HTML embedding."""
    raw_bytes = pil_to_bytes(image)
    return base64.b64encode(raw_bytes).decode("utf-8")


def speak_text_web(text: str, lang: str = "ru-RU", rate: float = 1.0):
    """
    Inject Web Speech API SpeechSynthesis JavaScript to speak text in browser.
    Works client-side without server TTS engine dependencies.
    """
    if not text.strip():
        return
        
    escaped_text = text.replace('"', '\\"').replace('\n', ' ')
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance("{escaped_text}");
            utterance.lang = "{lang}";
            utterance.rate = {rate};
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """
    st.components.v1.html(js_code, height=0)


def trigger_haptic_feedback():
    """Inject Navigator.vibrate API for sensory/haptic feedback."""
    js_code = """
    <script>
        if (navigator.vibrate) {
            navigator.vibrate([100, 50, 100]);
        }
    </script>
    """
    st.components.v1.html(js_code, height=0)


def format_timestamp(timestamp: Optional[float] = None) -> str:
    """Return formatted timestamp string for logging & history."""
    if timestamp is None:
        timestamp = time.time()
    return time.strftime("%H:%M:%S", time.localtime(timestamp))
