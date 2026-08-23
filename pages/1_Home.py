"""
VoxX - Page 1: Home (Главный экран)
Высококонтрастный доступный интерфейс (Черный фон, белый текст, желтый акцент #FFD700).
Сетка 2x2 крупных кнопок режимов.
"""
import sys
from pathlib import Path

# Ensure root package resolution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from core.session import init_session_state
from core.config import NAV_ITEMS

st.set_page_config(
    page_title="VoxX — Доступная Среда",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_session_state()

# Inject High-Contrast Accessible Custom CSS
st.markdown(
    """
    <style>
    /* Full Black Background & High Contrast Typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Top Accessibility Banner & Screenreader Title */
    .voxx-hero {
        text-align: left;
        padding: 10px 0 20px 0;
        border-bottom: 3px solid #FFD700;
        margin-bottom: 30px;
    }
    .voxx-title {
        color: #FFD700 !important;
        font-size: 64px !important;
        font-weight: 900 !important;
        margin: 0 !important;
        line-height: 1.1 !important;
        letter-spacing: -1px !important;
    }
    .voxx-subtitle {
        color: #FFFFFF !important;
        font-size: 24px !important;
        margin-top: 10px !important;
        font-weight: 500 !important;
    }

    /* 2x2 Large Accessibility Button Cards */
    div.stButton > button {
        min-height: 135px !important;
        width: 100% !important;
        background-color: #121212 !important;
        border: 4px solid #FFD700 !important;
        border-radius: 20px !important;
        color: #FFFFFF !important;
        padding: 22px 26px !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        text-align: left !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.15) !important;
        white-space: pre-wrap !important;
    }

    div.stButton > button:hover {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border-color: #FFFFFF !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(255, 215, 0, 0.45) !important;
    }

    div.stButton > button:focus, div.stButton > button:focus-visible {
        background-color: #FFD700 !important;
        color: #000000 !important;
        outline: 5px solid #FFFFFF !important;
        outline-offset: 4px !important;
    }

    /* Hide standard Streamlit header clutter */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section (Optimized for Screen Readers)
st.markdown(
    """
    <div class="voxx-hero" role="banner" aria-label="Главная страница ассистента VoxX">
        <h1 class="voxx-title">VoxX</h1>
        <p class="voxx-subtitle">Доступный инклюзивный помощник для людей с нарушениями слуха, зрения и речи</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='color: #FFD700; font-size: 28px; margin-bottom: 25px;'>Выберите режим работы:</h2>",
    unsafe_allow_html=True
)

# 2x2 Grid Layout
row1_col1, row1_col2 = st.columns(2, gap="large")

with row1_col1:
    btn_gestures = st.button(
        "🤟 1. ЖЕСТЫ\nРаспознавание жестового языка через камеру в реальном времени",
        key="btn_mode_gestures",
        help="Режим Жесты: Нажмите для перевода жестов видеокамеры в текст",
        use_container_width=True
    )
    if btn_gestures:
        st.session_state["active_mode"] = "gestures"
        st.session_state["current_mode"] = "Жесты"
        st.switch_page("pages/2_Жесты.py")

with row1_col2:
    btn_hearing = st.button(
        "👂 2. СЛУХ\nЖивые субтитры речи в текст и визуальный монитор шума",
        key="btn_mode_hearing",
        help="Режим Слух: Нажмите для распознавания речи в текст и мониторинга громкости",
        use_container_width=True
    )
    if btn_hearing:
        st.session_state["active_mode"] = "hearing"
        st.session_state["current_mode"] = "Слух"
        st.switch_page("pages/3_Слух.py")

row2_col1, row2_col2 = st.columns(2, gap="large")

with row2_col1:
    btn_vision = st.button(
        "👁️ 3. ЗРЕНИЕ\nСканирование текста с фото (OCR) и голосовая озвучка (TTS)",
        key="btn_mode_vision",
        help="Режим Зрение: Нажмите для чтения текста с фото и документации голосом",
        use_container_width=True
    )
    if btn_vision:
        st.session_state["active_mode"] = "vision"
        st.session_state["current_mode"] = "Зрение"
        st.switch_page("pages/4_Зрение.py")

with row2_col2:
    btn_universal = st.button(
        "💬 4. УНИВЕРСАЛЬНЫЙ\nБыстрые карточки фраз (AAC) и кнопка помощи SOS",
        key="btn_mode_universal",
        help="Режим Универсальный: Нажмите для общения крупными карточками и вызова SOS",
        use_container_width=True
    )
    if btn_universal:
        st.session_state["active_mode"] = "universal"
        st.session_state["current_mode"] = "Универсальный"
        st.switch_page("pages/5_Универсальный.py")

# Secondary Quick Navigation
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
sub_col1, sub_col2 = st.columns(2, gap="large")
with sub_col1:
    if st.button("⚙️ Настройки доступности", key="btn_home_settings", help="Персонализация шрифтов, цветов и речи"):
        st.session_state["active_mode"] = "settings"
        st.switch_page("pages/6_Настройки.py")
with sub_col2:
    if st.button("ℹ️ О приложении и диагностика", key="btn_home_about", help="Информация о платформе VoxX и проверка модулей"):
        st.session_state["active_mode"] = "about"
        st.switch_page("pages/7_О_приложении.py")
