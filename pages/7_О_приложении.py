"""
VoxX - Page 7: О приложении
Содержит информацию о версии (0.1.0), назначении, автономных (оффлайн) возможностях
и кнопку возврата на главный экран.
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

st.set_page_config(
    page_title="VoxX — О приложении",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
apply_custom_css()

# Top Header / Back Button
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("⬅️ На главную", key="btn_about_back_top", use_container_width=True):
        st.session_state["active_mode"] = "home"
        st.switch_page("pages/1_Home.py")

with col_title:
    st.markdown("<h1 style='margin: 0; color: #FFD700;'>ℹ️ О приложении VoxX</h1>", unsafe_allow_html=True)

st.markdown("---")

# Main Info Card
st.markdown(
    """
    <div style="
        background-color: #121212;
        border: 4px solid #FFD700;
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 25px;
        color: #FFFFFF;
    ">
        <h2 style="color: #FFD700; font-size: 36px; margin-top: 0;">VoxX (Версия 0.1.0)</h2>
        <p style="font-size: 24px; line-height: 1.6; font-weight: 500; color: #FFFFFF;">
            <strong>VoxX</strong> — это веб-платформа и инклюзивный ассистент, созданный для обеспечения 
            равного доступа к общению и информации людям с ограниченными возможностями здоровья.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col_target, col_offline = st.columns(2, gap="large")

with col_target:
    st.markdown(
        """
        <div style="
            background: #181818;
            border-left: 6px solid #00CEC9;
            border-radius: 16px;
            padding: 24px;
            min-height: 280px;
        ">
            <h3 style="color: #00CEC9; font-size: 26px; margin-top: 0;">🎯 Для кого предназначено:</h3>
            <ul style="font-size: 20px; line-height: 1.8; color: #FFFFFF;">
                <li><strong>Людям с нарушениями речи:</strong> карточки быстрых фраз (AAC) и озвучка в один клик.</li>
                <li><strong>Людям с нарушениями слуха:</strong> живые субтитры речи в текст и индикатор опасного уровня шума.</li>
                <li><strong>Людям с нарушениями зрения:</strong> сканирование текста с фото (OCR), экранный диктор и контрастный интерфейс.</li>
                <li><strong>Людям с нарушениями моторики:</strong> жестовое управление через веб-камеру.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_offline:
    st.markdown(
        """
        <div style="
            background: #181818;
            border-left: 6px solid #FFD700;
            border-radius: 16px;
            padding: 24px;
            min-height: 280px;
        ">
            <h3 style="color: #FFD700; font-size: 26px; margin-top: 0;">⚡ Что работает автономно (Оффлайн):</h3>
            <ul style="font-size: 20px; line-height: 1.8; color: #FFFFFF;">
                <li><strong>Распознавание жестов:</strong> локальная нейросеть MediaPipe выполняется прямо в браузере.</li>
                <li><strong>Синтез речи (TTS):</strong> встроенный браузерный движок Web Speech API / pyttsx3.</li>
                <li><strong>AAC Коммуникатор:</strong> полная база быстрых карточек фраз и система экстренных сигналов SOS.</li>
                <li><strong>Визуализатор шума:</strong> локальный анализ уровня дБ через веб-аудио API.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

if st.button("⬅️ Назад на главную", key="btn_about_back_bottom", use_container_width=True):
    st.session_state["active_mode"] = "home"
    st.switch_page("pages/1_Home.py")
