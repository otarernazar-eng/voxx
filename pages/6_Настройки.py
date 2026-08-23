"""
VoxX - Page 6: Настройки Доступности и Синтеза Речи
Персонализация размера шрифта, параметров голоса (TTS), высоты тона и контрастности.
"""
import sys
from pathlib import Path

# Ensure root package resolution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from core.session import init_session_state, reset_accessibility_settings
from core.theme import apply_custom_css
from shared.services.tts_service import TTSService

st.set_page_config(
    page_title="VoxX — Настройки Доступности",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
apply_custom_css()

if "tts_service" not in st.session_state:
    st.session_state.tts_service = TTSService()

tts: TTSService = st.session_state.tts_service

# Header & Navigation Back Button
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("⬅️ На главную", key="btn_settings_back_top", use_container_width=True):
        st.session_state["active_mode"] = "home"
        st.switch_page("pages/1_Home.py")

with col_title:
    st.markdown("<h1 style='margin: 0; color: #FFD700;'>⚙️ Настройки Доступности</h1>", unsafe_allow_html=True)

st.markdown("---")

col_vis, col_audio = st.columns(2, gap="large")

with col_vis:
    st.markdown(
        """
        <div style="background: #121212; border: 3px solid #FFD700; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: #FFD700; margin-top: 0;">👁️ Настройки Отображения</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 1. Font Size Slider (1.0 to 2.0)
    current_font_scale = float(st.session_state.get("font_size_scale", 1.0))
    new_font_scale = st.slider(
        "🔤 Масштаб шрифта и элементов (от 1.0 до 2.0):",
        min_value=1.0,
        max_value=2.0,
        value=current_font_scale,
        step=0.1,
        help="Увеличьте слайдер для более крупного отображения всех надписей и кнопок",
        key="slider_font_scale"
    )
    if new_font_scale != current_font_scale:
        st.session_state["font_size_scale"] = new_font_scale
        st.rerun()

    # 2. High Contrast Toggle (Default ON)
    current_hc = st.session_state.get("high_contrast", True)
    new_hc = st.toggle(
        "👁️‍🗨️ Высокий контраст (Черно-желтый интерфейс)",
        value=current_hc,
        help="Обеспечивает максимальную контрастность текста и яркие желтые акценты",
        key="toggle_high_contrast"
    )
    if new_hc != current_hc:
        st.session_state["high_contrast"] = new_hc
        st.rerun()

    # 3. Screen Reader Simplified Interface
    current_sr = st.session_state.get("screenreader_mode", False)
    new_sr = st.toggle(
        "🦯 Упрощённый интерфейс для незрячих (Screen Reader)",
        value=current_sr,
        help="Увеличивает жирность шрифта и оптимизирует порядок элементов для программам чтения экрана",
        key="toggle_screenreader"
    )
    if new_sr != current_sr:
        st.session_state["screenreader_mode"] = new_sr
        st.rerun()

with col_audio:
    # =========================================================================
    # Промпт 5.3 — Настройки голоса и Синтеза Речи (TTS)
    # =========================================================================
    st.markdown(
        """
        <div style="background: #121212; border: 3px solid #00CEC9; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: #00CEC9; margin-top: 0;">🔊 Настройки Голоса и Синтеза Речи (TTS)</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Выбор системного или браузерного голоса
    voices = tts.get_available_voices()
    voice_names = [v["name"] for v in voices]
    selected_voice_name = st.selectbox(
        "🎙️ Выбор диктора / голоса:",
        options=voice_names,
        index=0,
        help="Выберите голос для воспроизведения сообщений",
        key="select_voice"
    )

    # Слайдер скорости речи (0.5 до 2.0)
    current_rate = float(st.session_state.get("tts_speed_rate", 1.0))
    new_rate = st.slider(
        "⚡ Скорость речи (от 0.5 до 2.0):",
        min_value=0.5,
        max_value=2.0,
        value=current_rate,
        step=0.1,
        help="Настройте комфортную скорость озвучки голосового диктора",
        key="slider_tts_rate"
    )
    st.session_state["tts_speed_rate"] = new_rate
    tts.set_rate(new_rate)

    # Слайдер высоты тона (0.5 до 2.0)
    current_pitch = float(st.session_state.get("tts_pitch", 1.0))
    new_pitch = st.slider(
        "🎵 Высота тона голоса (от 0.5 до 2.0):",
        min_value=0.5,
        max_value=2.0,
        value=current_pitch,
        step=0.1,
        help="Регулирует тембр голосового диктора (более низкий или высокий тон)",
        key="slider_tts_pitch"
    )
    st.session_state["tts_pitch"] = new_pitch
    tts.set_pitch(new_pitch)

    # Слайдер громкости (0.0 до 1.0)
    current_vol = float(st.session_state.get("tts_volume", 1.0))
    new_vol = st.slider(
        "🔊 Громкость диктора (от 0.0 до 1.0):",
        min_value=0.0,
        max_value=1.0,
        value=current_vol,
        step=0.1,
        help="Регулирует громкость воспроизведения речи",
        key="slider_tts_volume"
    )
    st.session_state["tts_volume"] = new_vol
    tts.set_volume(new_vol)

    # Промпт 5.3 — Кнопка «Прослушать пример»
    if st.button("🔊 Прослушать пример речи", key="btn_test_speech", use_container_width=True):
        sample_text = "Здравствуйте! Это тестовая озвучка голоса приложения VoxX."
        tts.speak(sample_text)
        st.success(f"Воспроизводится тестовая фраза: «{sample_text}»")

st.markdown("---")

col_rst, col_back_bot = st.columns(2, gap="large")

with col_rst:
    if st.button("🔄 Сбросить настройки", key="btn_reset_settings_page", use_container_width=True):
        reset_accessibility_settings()
        st.success("Все настройки сброшены!")
        st.rerun()

with col_back_bot:
    if st.button("⬅️ Назад на главную", key="btn_settings_back_bottom", use_container_width=True):
        st.session_state["active_mode"] = "home"
        st.switch_page("pages/1_Home.py")
