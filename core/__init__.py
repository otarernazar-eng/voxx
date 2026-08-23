"""
VoxX Core Module
"""
from core.config import APP_NAME, APP_VERSION, COLORS
from core.session import init_session_state, add_gesture_to_history
from core.theme import apply_custom_css

__all__ = ["APP_NAME", "APP_VERSION", "COLORS", "init_session_state", "add_gesture_to_history", "apply_custom_css"]
