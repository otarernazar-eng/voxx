"""
VoxX - Page 5: Универсальный
"""
import streamlit as st
from voxx.core.session import init_session_state
from voxx.core.theme import apply_custom_css
from voxx.shared.components.header import render_app_header
from voxx.features.universal.presentation.universal_view import render_universal_screen

st.set_page_config(
    page_title="VoxX — Универсальный Коммуникатор",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
apply_custom_css()

render_app_header(title_suffix="— AAC Коммуникация", icon="💬")
render_universal_screen()
