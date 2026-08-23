"""
===============================================================================
VoxX - Vision Assistant View (Модуль 7)
Описание окружения, автоописание каждые 3 сек, чтение текста (OCR) и распознавание купюр.
===============================================================================
"""
import sys
import time
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Path configuration for root imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.session import init_session_state
from shared.services.camera_service import CameraService
from shared.services.vision_service import VisionService
from shared.services.tts_service import TTSService


def render_vision_screen():
    """
    Главный интерфейс ассистента зрения и распознавания объектов.
    """
    init_session_state()

    # Инициализация session_state
    if "auto_describe_active" not in st.session_state:
        st.session_state.auto_describe_active = False
    if "read_text_ocr_mode" not in st.session_state:
        st.session_state.read_text_ocr_mode = False
    if "last_vision_description" not in st.session_state:
        st.session_state.last_vision_description = ""
    if "vision_zoom_level" not in st.session_state:
        st.session_state.vision_zoom_level = 1.0

    # Инициализация сервисов
    if "vision_service" not in st.session_state:
        st.session_state.vision_service = VisionService()
    if "tts_service" not in st.session_state:
        st.session_state.tts_service = TTSService()

    vision: VisionService = st.session_state.vision_service
    tts: TTSService = st.session_state.tts_service

    # =========================================================================
    # Верхняя Панель Настроек Режима (Промпт 7.3 & 7.4)
    # =========================================================================
    col_t1, col_t2, col_t3 = st.columns([1.2, 1.2, 1.0])

    with col_t1:
        # Промпт 7.3 — Автоописание каждые 3-4 секунды
        st.session_state.auto_describe_active = st.toggle(
            "🔄 Автоописание (каждые 3 сек)",
            value=st.session_state.auto_describe_active,
            help="Автоматически сканировать окружение каждые 3 секунды"
        )

    with col_t2:
        # Промпт 7.4 — Режим Читать Текст
        st.session_state.read_text_ocr_mode = st.toggle(
            "📖 Режим «Читать текст» (OCR)",
            value=st.session_state.read_text_ocr_mode,
            help="Поиск и распознавание печатных надписей"
        )

    with col_t3:
        if st.session_state.auto_describe_active:
            st.markdown(
                """
                <div style="
                    background: #121212;
                    border: 2px solid #00B894;
                    border-radius: 12px;
                    padding: 6px;
                    text-align: center;
                    color: #00B894;
                    font-weight: bold;
                    font-size: 16px;
                ">
                    🟢 Автоописание активно
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # =========================================================================
    # Главные Кнопки Действий (Высота ≥ 65px)
    # =========================================================================
    st.markdown(
        """
        <style>
        .stButton > button[kind="primary"] {
            background-color: #00B894 !important;
            min-height: 65px !important;
            font-size: 22px !important;
        }
        .stButton > button[kind="secondary"] {
            min-height: 65px !important;
            font-size: 20px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    btn_v1, btn_v2, btn_v3 = st.columns(3, gap="medium")

    should_analyze_now = False
    recognize_banknote_now = False

    with btn_v1:
        if st.button("📷 ОПИСАТЬ ОКРУЖЕНИЕ", key="btn_describe_now", type="primary", use_container_width=True):
            should_analyze_now = True

    with btn_v2:
        if st.button("📖 ПРОЧИТАТЬ ТЕКСТ", key="btn_read_text_now", use_container_width=True):
            st.session_state.read_text_ocr_mode = True
            should_analyze_now = True

    with btn_v3:
        # Промпт 7.5 — Кнопка «Распознать купюру»
        if st.button("💵 РАСПОЗНАТЬ КУПЮРУ", key="btn_banknote_now", use_container_width=True):
            recognize_banknote_now = True

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # Зум слайдер (Промпт 7.4)
    zoom = st.slider("🔍 Зум предпросмотра (от 1.0x до 3.0x):", min_value=1.0, max_value=3.0, value=float(st.session_state.vision_zoom_level), step=0.5, key="slider_vision_zoom")
    st.session_state.vision_zoom_level = zoom

    # =========================================================================
    # Камера и Анализ Изображения
    # =========================================================================
    main_col, info_col = st.columns([1.6, 1.0])

    analysis_result = None

    with main_col:
        cam_input = st.camera_input("Камера Зрения", key="vision_cam_feed")

        if cam_input:
            frame_bgr = CameraService.decode_streamlit_image(cam_input)

            if frame_bgr is not None:
                # Ограничение зума
                if zoom > 1.0:
                    h, w, c = frame_bgr.shape
                    new_h, new_w = int(h / zoom), int(w / zoom)
                    top, left = (h - new_h) // 2, (w - new_w) // 2
                    cropped = frame_bgr[top:top+new_h, left:left+new_w]
                    frame_bgr = cv2.resize(cropped, (w, h))

                # Автоописание каждые 3 секунды
                if st.session_state.auto_describe_active or should_analyze_now:
                    analysis_result = vision.analyze(frame_bgr)
                    st.session_state.last_analysis_result = analysis_result

                    desc = analysis_result["description"]

                    # Озвучивание если описание изменилось или при прямом нажатии
                    if desc != st.session_state.last_vision_description or should_analyze_now:
                        st.session_state.last_vision_description = desc
                        tts.speak(desc)

                # Промпт 7.5 — Обработка банкноты
                if recognize_banknote_now:
                    banknote_msg = vision.recognize_banknote(frame_bgr)
                    tts.speak(banknote_msg)
                    st.warning(f"💵 {banknote_msg}")

        else:
            st.info("💡 Нажмите снимок камеры для анализа сцены...")

    with info_col:
        st.markdown("### 📊 Описание Сцены (Результат)")

        result = st.session_state.get("last_analysis_result", None)

        if result:
            desc_text = result.get("description", "Ничего не найдено")

            st.markdown(
                f"""
                <div style="
                    background: #121212;
                    border: 4px solid #FFD700;
                    border-radius: 20px;
                    padding: 20px;
                    margin-bottom: 20px;
                " role="region" aria-label="Результат описания сцены: {desc_text}">
                    <p style="color: #A0A0B2; margin: 0; font-size: 14px;">Описание окружения:</p>
                    <h2 style="color: #FFD700; font-size: 28px; margin: 8px 0;">{desc_text}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Промпт 7.4 — Текстовые блоки OCR
            text_blocks = result.get("text_blocks", [])
            if text_blocks:
                st.markdown(f"#### 📖 Распознанные блоки текста ({len(text_blocks)}):")
                for b_idx, block in enumerate(text_blocks):
                    b_col1, b_col2 = st.columns([3, 1])
                    with b_col1:
                        st.markdown(f"• **{block['text']}** ({int(block['confidence']*100)}%)")
                    with b_col2:
                        if st.button("🔊", key=f"btn_speak_block_{b_idx}"):
                            tts.speak(block['text'])

                if st.button("🔊 Озвучить весь текст", key="btn_speak_all_ocr", use_container_width=True):
                    tts.speak(result.get("text", ""))

        else:
            st.info("Нажмите **📷 ОПИСАТЬ ОКРУЖЕНИЕ** для первого снимка.")
