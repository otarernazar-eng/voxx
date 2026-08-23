"""
===============================================================================
VoxX - Camera Gestures Integration Component (Модули 2, 3, 4, 5)
Видеопоток, MediaPipe, оверлей, классификация жестов, автоозвучка, 
очередь речи TTS и кнопки воспроизведения/повтора.
===============================================================================
"""
import io
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, List

import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Path configuration for root imports
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.session import init_session_state, add_gesture_to_history
from shared.services.camera_service import CameraService
from shared.services.pose_hand_service import PoseHandService, normalize_landmarks, LandmarkBuffer
from shared.services.tts_service import TTSService
from features.gestures.domain.gesture_classifier import RuleBasedGestureClassifier
from features.gestures.domain.gesture_dictionary import GESTURE_DICTIONARY, search_gestures


def apply_gesture_overlay(frame_bgr: np.ndarray, text_hint: str = "ПОКАЖИТЕ ЖЕСТЫ В РАМКУ") -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    """Промпт 2.2 — Оверлей с жёлтой рамкой 70% x 50%."""
    if frame_bgr is None:
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        return blank, (0, 0, 0, 0)

    h, w, c = frame_bgr.shape
    rw, rh = int(w * 0.70), int(h * 0.50)
    x1, y1 = (w - rw) // 2, (h - rh) // 2
    x2, y2 = x1 + rw, y1 + rh

    mask = frame_bgr.copy()
    cv2.rectangle(mask, (0, 0), (w, h), (0, 0, 0), -1)
    mask[y1:y2, x1:x2] = frame_bgr[y1:y2, x1:x2]

    annotated = cv2.addWeighted(frame_bgr, 0.6, mask, 0.4, 0)
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 215, 255), 5)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale, thickness = 0.8, 2
    (tw, th), _ = cv2.getTextSize(text_hint, font, font_scale, thickness)
    tx, ty = (w - tw) // 2, max(y1 - 15, 35)

    cv2.putText(annotated, text_hint, (tx + 2, ty + 2), font, font_scale, (0, 0, 0), thickness + 2)
    cv2.putText(annotated, text_hint, (tx, ty), font, font_scale, (255, 255, 255), thickness)

    return annotated, (x1, y1, x2, y2)


def render_camera_gestures_page():
    """
    Главный интерфейс распознавания жестов, управления автоозвучкой и TTS речью.
    """
    init_session_state()

    # Инициализация session_state
    if "camera_active" not in st.session_state:
        st.session_state.camera_active = True
    if "camera_facing_mode" not in st.session_state:
        st.session_state.camera_facing_mode = "user"
    if "last_captured_frame" not in st.session_state:
        st.session_state.last_captured_frame = None
    if "recorded_video_bytes" not in st.session_state:
        st.session_state.recorded_video_bytes = None
    
    # Промпт 4.3 — De-duplication
    if "last_gesture_time" not in st.session_state:
        st.session_state.last_gesture_time = 0.0
    if "last_recognized_name" not in st.session_state:
        st.session_state.last_recognized_name = ""

    # Промпт 4.4 — Накопление фразы
    if "accumulation_mode" not in st.session_state:
        st.session_state.accumulation_mode = True
    if "accumulated_words" not in st.session_state:
        st.session_state.accumulated_words = []

    # Промпт 5.2 — Переключатель автоозвучки
    if "auto_tts_enabled" not in st.session_state:
        st.session_state.auto_tts_enabled = False

    # Промпт 5.5 — Последняя произнесенная фраза
    if "last_spoken_phrase" not in st.session_state:
        st.session_state.last_spoken_phrase = ""

    # Инициализация сервисов
    if "pose_hand_service" not in st.session_state:
        st.session_state.pose_hand_service = PoseHandService(max_hands=2, buffer_capacity=30)
    if "gesture_classifier" not in st.session_state:
        st.session_state.gesture_classifier = RuleBasedGestureClassifier()
    if "tts_service" not in st.session_state:
        st.session_state.tts_service = TTSService()

    pose_service: PoseHandService = st.session_state.pose_hand_service
    classifier: RuleBasedGestureClassifier = st.session_state.gesture_classifier
    tts: TTSService = st.session_state.tts_service

    # =========================================================================
    # Верхняя Панель Индикации Камеры и Очереди Речи TTS (Промпт 5.4)
    # =========================================================================
    is_active = st.session_state.camera_active
    status_icon = "🟢" if is_active else "⚪"
    status_text = "Камера включена" if is_active else "Камера выключена"
    status_border = "#00B894" if is_active else "#A0A0B2"
    buffer_count = pose_service.buffer.current_size
    queue_len = tts.get_queue_length()

    st.markdown(
        f"""
        <div style="
            background-color: #121212;
            border: 3px solid {status_border};
            border-radius: 16px;
            padding: 16px 20px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        " role="status" aria-label="Статус камеры: {status_text}">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 28px;">{status_icon}</span>
                <div>
                    <h3 style="margin: 0; font-size: 22px; color: #FFFFFF;">{status_text}</h3>
                    <p style="margin: 0; color: #A0A0B2; font-size: 14px;">
                        Камера: <strong>{st.session_state.camera_facing_mode.upper()}</strong>
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 12px;">
                <div style="background: #1E1E1E; border: 2px solid #FFD700; border-radius: 12px; padding: 6px 14px;">
                    <span style="color: #FFD700; font-weight: bold; font-size: 16px;">
                        📊 Буфер: {buffer_count}/30
                    </span>
                </div>
                <div style="background: #1E1E1E; border: 2px solid #00CEC9; border-radius: 12px; padding: 6px 14px;">
                    <span style="color: #00CEC9; font-weight: bold; font-size: 16px;">
                        🔊 Очередь речи: {queue_len}/10
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Панель управления камерой и переключателями
    st.markdown("<style>div.stButton > button { min-height: 55px !important; font-size: 18px !important; }</style>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1.2, 1.2])
    with c1:
        if is_active:
            if st.button("⏹️ СТОП", key="btn_cam_stop", help="Остановить поток"):
                st.session_state.camera_active = False
                st.rerun()
        else:
            if st.button("▶️ ЗАПУСТИТЬ", key="btn_cam_start", help="Запустить поток"):
                st.session_state.camera_active = True
                st.rerun()

    with c2:
        if st.button("⚡ БЫСТРЫЙ ЗАПУСК", key="btn_cam_quick_start", help="Ускоренный перезапуск"):
            st.session_state.camera_active = True
            st.rerun()

    with c3:
        if st.button("🔄 ПЕРЕКЛЮЧИТЬ", key="btn_cam_switch", help="Переключить камеру"):
            st.session_state.camera_facing_mode = "environment" if st.session_state.camera_facing_mode == "user" else "user"
            st.rerun()

    with c4:
        st.session_state.accumulation_mode = st.toggle(
            "📝 Накопление фразы",
            value=st.session_state.accumulation_mode,
            help="Собирать распознанные слова в предложение"
        )

    with c5:
        # Промпт 5.2 — Переключатель Автоозвучки
        st.session_state.auto_tts_enabled = st.toggle(
            "🔊 Автоозвучка",
            value=st.session_state.auto_tts_enabled,
            help="Автоматически произносить каждое новое распознанное слово"
        )

    st.markdown("---")

    # =========================================================================
    # Главная Зона Предпросмотра
    # =========================================================================
    main_view_col, side_info_col = st.columns([1.6, 1.0])

    with main_view_col:
        st.markdown(
            "### 📷 Видеопоток распознавания жестов\n"
            "<span style='color:#FFD700; font-size:16px;' aria-label='Инструкция'>"
            "📍 Держите жест 2 секунды внутри жёлтой рамки</span>",
            unsafe_allow_html=True
        )

        if st.session_state.camera_active:
            cam_input = st.camera_input("Камера", key="cam_feed_m5")

            if cam_input:
                frame_bgr = CameraService.decode_streamlit_image(cam_input)

                if frame_bgr is not None:
                    overlayed_bgr, _ = apply_gesture_overlay(frame_bgr)
                    is_front = (st.session_state.camera_facing_mode == "user")
                    pose_result = pose_service.process_frame(overlayed_bgr, is_front_camera=is_front)

                    annotated_frame = pose_result["annotated_frame"]
                    buffer_items = pose_service.buffer.get_all()

                    detected_gesture_result = classifier.classify(buffer_items)

                    if detected_gesture_result:
                        g_name = detected_gesture_result["name"]
                        g_sym = detected_gesture_result.get("symbol", "🤟")
                        display_str = f"{g_sym} {g_name}"

                        cv2.putText(
                            annotated_frame,
                            display_str,
                            (30, annotated_frame.shape[0] - 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.2,
                            (0, 215, 255),
                            3
                        )

                        now = time.time()
                        if (now - st.session_state.last_gesture_time > 2.0) or (g_name != st.session_state.last_recognized_name):
                            st.session_state.last_gesture_time = now
                            st.session_state.last_recognized_name = g_name
                            add_gesture_to_history(g_name, detected_gesture_result["confidence"])

                            clean_word = g_name.split("/")[0].strip()

                            if st.session_state.accumulation_mode:
                                st.session_state.accumulated_words.append(clean_word)

                            # Промпт 5.2 — Автоматическое озвучивание жеста при автоозвучке
                            if st.session_state.auto_tts_enabled:
                                tts.speak(clean_word)

                    st.image(
                        annotated_frame,
                        caption="Распознавание жестов в реальном времени (MediaPipe)",
                        use_container_width=True
                    )

                    try:
                        st.session_state.last_captured_frame = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                    except Exception:
                        pass
            else:
                st.info("💡 Ожидание разрешения браузера и видеопотока...")
        else:
            st.warning("⚠️ Камера остановлена.")

        # Отображение распознанного жеста
        if st.session_state.last_recognized_name:
            st.markdown(
                f"""
                <div style="
                    background: #121212;
                    border: 4px solid #FFD700;
                    border-radius: 20px;
                    padding: 16px;
                    margin-top: 15px;
                    text-align: center;
                " role="region" aria-label="Распознан жест: {st.session_state.last_recognized_name}">
                    <p style="color: #A0A0B2; margin: 0; font-size: 15px;">Последний распознанный жест:</p>
                    <h1 style="color: #FFD700; font-size: 40px; margin: 4px 0;">{st.session_state.last_recognized_name}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Накопленная фраза
        st.markdown("### 💬 Накопленная фраза:")
        current_phrase = " ".join(st.session_state.accumulated_words)

        st.markdown(
            f"""
            <div style="
                background: #181818;
                border: 3px solid #00CEC9;
                border-radius: 16px;
                padding: 18px;
                min-height: 75px;
                font-size: 28px;
                font-weight: bold;
                color: #FFFFFF;
            " role="region" aria-label="Текущая накопленная фраза: {current_phrase or 'Пусто'}">
                {current_phrase if current_phrase else '<span style="color: #777777; font-style: italic;">Фраза пока пуста. Показывайте жесты...</span>'}
            </div>
            """,
            unsafe_allow_html=True
        )

        phrase_col1, phrase_col2 = st.columns(2)
        with phrase_col1:
            if st.button("⌫ Удалить последнее слово", key="btn_del_last", help="Удалить последнее добавленное слово"):
                if st.session_state.accumulated_words:
                    st.session_state.accumulated_words.pop()
                    st.rerun()
        with phrase_col2:
            if st.button("🧹 Очистить фразу", key="btn_clr_phrase", help="Очистить накопленный текст"):
                st.session_state.accumulated_words.clear()
                st.rerun()

        # =========================================================================
        # Промпт 5.5 — Кнопки «🔊 Озвучить фразу», «🔁 Повторить» и «🗑️ Очистить»
        # Крупные кнопки высотой ≥ 65px
        # =========================================================================
        st.markdown(
            """
            <style>
            .stButton > button[kind="primary"] {
                background-color: #00B894 !important;
                color: #FFFFFF !important;
                border-color: #00CEC9 !important;
                min-height: 65px !important;
                font-size: 22px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        bot_col1, bot_col2, bot_col3 = st.columns(3, gap="medium")

        with bot_col1:
            has_phrase = bool(current_phrase.strip())
            if st.button(
                "🔊 Озвучить фразу",
                key="btn_speak_phrase",
                disabled=not has_phrase,
                type="primary",
                help="Произнести накопленную фразу голосом через синтезатор речи (TTS)"
            ):
                tts.speak(current_phrase)
                st.success(f"🔊 Озвучивается: «{current_phrase}»")

        with bot_col2:
            # Промпт 5.5 — Кнопка «Повторить последнюю фразу»
            last_spoken = st.session_state.get("last_spoken_phrase", "")
            has_last = bool(last_spoken.strip())
            if st.button(
                "🔁 Повторить фразу",
                key="btn_repeat_phrase",
                disabled=not has_last,
                help="Повторить последнюю произнесённую фразу голосом"
            ):
                tts.speak(last_spoken)
                st.info(f"🔁 Повтор речи: «{last_spoken}»")

        with bot_col3:
            if st.button(
                "🗑️ Сбросить всё",
                key="btn_clear_all_phrase",
                disabled=not has_phrase,
                help="Полностью сбросить накопленную фразу"
            ):
                st.session_state.accumulated_words.clear()
                st.rerun()

    with side_info_col:
        # Словарь жестов РЖЯ (25 жестов)
        st.markdown("### 📖 Словарь жестов РЖЯ")
        search_query = st.text_input("🔍 Поиск жеста:", value="", placeholder="Привет, Вода...", key="dict_search_m5")
        dictionary_results = search_gestures(search_query)

        st.markdown(f"**Найдено жестов: {len(dictionary_results)} из {len(GESTURE_DICTIONARY)}**")
        dict_container = st.container(height=360)
        with dict_container:
            for item in dictionary_results:
                st.markdown(
                    f"""
                    <div style="
                        background: #1A1A2E;
                        border-left: 4px solid #FFD700;
                        padding: 10px 14px;
                        border-radius: 10px;
                        margin-bottom: 8px;
                    ">
                        <strong style="color: #FFD700; font-size: 18px;">{item['symbol']} {item['name']}</strong>
                        <span style="font-size: 12px; color: #00CEC9; margin-left: 8px;">({item['category']})</span>
                        <p style="margin: 4px 0 0 0; font-size: 13px; color: #D0D0E0;">{item['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
