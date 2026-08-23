"""
===============================================================================
VoxX - Hearing Assistant View (Модуль 6)
Преобразование речи в текст (STT), живые субтитры (≥32px), режим "Только текст",
история последних 50 фраз с озвучкой и визуально-вибрационный сигнал о новом тексте.
===============================================================================
"""
import sys
import time
from pathlib import Path
import streamlit as st

# Path configuration for root imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.session import init_session_state
from shared.services.stt_service import STTService
from shared.services.tts_service import TTSService


def render_hearing_screen():
    """
    Главная страница ассистента слуха и живых субтитров.
    """
    init_session_state()

    # Инициализация session_state
    if "stt_is_listening" not in st.session_state:
        st.session_state.stt_is_listening = False
    if "stt_transcript_history" not in st.session_state:
        st.session_state.stt_transcript_history = []
    if "text_only_mode" not in st.session_state:
        st.session_state.text_only_mode = True
    if "stt_new_text_signal" not in st.session_state:
        st.session_state.stt_new_text_signal = True
    if "current_live_transcript" not in st.session_state:
        st.session_state.current_live_transcript = ""

    # Инициализация сервисов
    if "stt_service" not in st.session_state:
        st.session_state.stt_service = STTService()
    if "tts_service" not in st.session_state:
        st.session_state.tts_service = TTSService()

    stt: STTService = st.session_state.stt_service
    tts: TTSService = st.session_state.tts_service

    # =========================================================================
    # Верхняя Панель Настройки Режима (Промпт 6.4)
    # =========================================================================
    st_col1, st_col2, st_col3 = st.columns([1.5, 1, 1])

    with st_col1:
        st.session_state.text_only_mode = st.toggle(
            "📱 Режим «Только текст» (Максимальная доступность)",
            value=st.session_state.text_only_mode,
            help="Упрощенный высококонтрастный интерфейс без камеры"
        )

    with st_col2:
        st.session_state.stt_new_text_signal = st.toggle(
            "📳 Сигнал при новом тексте",
            value=st.session_state.stt_new_text_signal,
            help="Визуальная вспышка и вибрация браузера при появлении новой фразы"
        )

    with st_col3:
        is_listening = st.session_state.stt_is_listening
        status_color = "#00B894" if is_listening else "#FF7675"
        status_text = "Слушаю..." if is_listening else "Остановлено"
        st.markdown(
            f"""
            <div style="
                background: #121212;
                border: 2px solid {status_color};
                border-radius: 12px;
                padding: 6px 14px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                color: {status_color};
            ">
                {status_text}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # =========================================================================
    # Крупная Кнопка Старта / Остановки и Записи (Промпт 6.2)
    # Высота ≥ 65px
    # =========================================================================
    st.markdown(
        """
        <style>
        .stButton > button[kind="primary"] {
            background-color: #00B894 !important;
            min-height: 65px !important;
            font-size: 24px !important;
        }
        .stButton > button[kind="secondary"] {
            min-height: 65px !important;
            font-size: 22px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    btn_col1, btn_col2 = st.columns(2, gap="large")

    with btn_col1:
        if not st.session_state.stt_is_listening:
            if st.button("🎙️ НАЧАТЬ СЛУШАТЬ", key="btn_stt_start_main", type="primary", use_container_width=True):
                st.session_state.stt_is_listening = True
                stt.start_listening()
                st.rerun()
        else:
            if st.button("⏹️ СТОП СЛУШАТЬ", key="btn_stt_stop_main", use_container_width=True):
                st.session_state.stt_is_listening = False
                stt.stop_listening()
                st.rerun()

    with btn_col2:
        # Ввод фразы вручную (для отладки и быстрого добавления речи)
        manual_input = st.text_input("💬 Симуляция / Быстрый ввод речи:", value="", placeholder="Введите текст...", key="input_stt_manual")
        if manual_input and st.button("➕ Добавить в живые субтитры", key="btn_add_manual"):
            new_item = {
                "timestamp": time.strftime("%H:%M:%S", time.localtime()),
                "text": manual_input.strip()
            }
            # Сохранение последних 50 фраз (Промпт 6.3)
            st.session_state.stt_transcript_history.insert(0, new_item)
            if len(st.session_state.stt_transcript_history) > 50:
                st.session_state.stt_transcript_history.pop()

            st.session_state.current_live_transcript = manual_input.strip()
            
            # Промпт 6.5 — Вибрационный и визуальный сигнал
            if st.session_state.stt_new_text_signal:
                st.components.v1.html(
                    "<script>if('vibrate' in navigator){navigator.vibrate([100, 50, 100]);}</script>",
                    height=0
                )
            st.rerun()

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Интеграция веб-компонента Web Speech API
    if st.session_state.stt_is_listening:
        stt.render_browser_stt_component()

    # =========================================================================
    # Промпт 6.2 — Главное Окно Распознанного Текста (Шрифт ≥ 32px)
    # =========================================================================
    st.markdown("### 📜 Живые субтитры речи:")

    current_text = st.session_state.current_live_transcript
    flash_border = "#FFD700" if (st.session_state.stt_new_text_signal and current_text) else "#00CEC9"

    st.markdown(
        f"""
        <div style="
            background-color: #000000;
            border: 4px solid {flash_border};
            border-radius: 20px;
            padding: 28px;
            min-height: 160px;
            max-height: 300px;
            overflow-y: auto;
            color: #FFFFFF;
            font-size: 34px;
            font-weight: 800;
            line-height: 1.5;
            box-shadow: 0 8px 30px rgba(255, 215, 0, 0.2);
        " role="log" aria-live="polite" aria-label="Субтитры распознанной речи">
            {f'<span style="color: #FFD700;">{current_text}</span>' if current_text else '<span style="color: #A0A0B2; font-size: 28px; font-weight: normal;">Нажмите «🎙️ НАЧАТЬ СЛУШАТЬ» или введите текст выше...</span>'}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # Промпт 6.3 — История Последних Фраз (Хранение 50 фраз, Вывод 8-10)
    # =========================================================================
    hist_header_col, hist_clear_col = st.columns([3, 1])

    with hist_header_col:
        st.markdown(f"### 🕒 История последних фраз (Всего: {len(st.session_state.stt_transcript_history)} / 50)")

    with hist_clear_col:
        if st.button("🧹 Очистить историю", key="btn_clear_stt_hist", use_container_width=True):
            st.session_state.stt_transcript_history.clear()
            st.session_state.current_live_transcript = ""
            st.rerun()

    history_items = st.session_state.stt_transcript_history[:10]  # Показываем последние 8-10

    if history_items:
        for idx, item in enumerate(history_items):
            h_col1, h_col2 = st.columns([4, 1])
            with h_col1:
                st.markdown(
                    f"""
                    <div style="
                        background: #181818;
                        border-left: 5px solid #FFD700;
                        border-radius: 12px;
                        padding: 14px 18px;
                        margin-bottom: 8px;
                    ">
                        <span style="color: #A0A0B2; font-size: 14px;">[{item['timestamp']}]</span>
                        <p style="margin: 4px 0 0 0; font-size: 22px; font-weight: 600; color: #FFFFFF;">
                            {item['text']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with h_col2:
                # Нажатие на фразу озвучивает её через TTS (Промпт 6.3)
                if st.button("🔊 Озвучить", key=f"btn_speak_hist_{idx}", use_container_width=True):
                    tts.speak(item['text'])
                    st.info(f"🔊 Озвучивается: «{item['text']}»")
    else:
        st.info("История распознанных фраз пока пуста.")
