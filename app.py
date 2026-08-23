"""
===============================================================================
VoxX - Web Platform Entry Point
===============================================================================
"""
import sys
from pathlib import Path

# Add root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from core.session import init_session_state

st.set_page_config(
    page_title="VoxX — Доступная Среда",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_session_state()

# Automatically redirect to primary accessible Home page
st.switch_page("pages/1_Home.py")

