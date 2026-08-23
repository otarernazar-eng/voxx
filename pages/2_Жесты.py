"""
VoxX - Page 2: Жесты (Интеграция Камеры и Распознавание Жестов)
"""
import sys
from pathlib import Path

# Ensure root package resolution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from core.session import init_session_state
from core.theme import apply_custom_css
from shared.components.header import render_app_header
from shared.services.permissions import render_permission_explanation
from features.gestures.presentation.camera_page import render_camera_gestures_page

st.set_page_config(
    page_title="VoxX — Распознавание жестов",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
apply_custom_css()

render_permission_explanation()
render_app_header(title_suffix="— Распознавание Жестов", icon="🤟")
render_camera_gestures_page()
