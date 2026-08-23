"""
Presentation layer for Gesture Recognition feature screen
"""
import streamlit as st
from voxx.features.gestures.domain.gesture_detector import GestureDetector
from voxx.shared.services.camera_service import CameraService
from voxx.core.session import add_gesture_to_history
from voxx.shared.models.gesture_model import GESTURE_DICTIONARY


def render_gestures_screen():
    """Render full gesture recognition feature interface."""
    st.markdown("## 🤟 Распознавание Жестового Языка")
    st.markdown(
        "Используйте веб-камеру или загрузите снимок для автоматического "
        "перевода жестов в текст и голосовое воспроизведение."
    )

    detector = GestureDetector()

    col_cam, col_info = st.columns([1.6, 1.0])

    with col_cam:
        st.markdown("### 📷 Входной видеопоток")
        camera_input = st.camera_input("Снимите жест на камеру", key="gesture_cam_input")

        if camera_input:
            frame_bgr = CameraService.decode_streamlit_image(camera_input)
            if frame_bgr is not None:
                annotated_rgb, gesture, conf = detector.process_frame(frame_bgr)
                st.image(annotated_rgb, caption="Анализ ключевых точек руки (MediaPipe)", use_container_width=True)

                if gesture:
                    add_gesture_to_history(gesture.name, conf)
                    st.success(f"Распознан жест: **{gesture.symbol} {gesture.name}** ({int(conf * 100)}%)")

    with col_info:
        st.markdown("### 📊 Статус распознавания")
        last_gesture = st.session_state.get("last_detected_gesture", "Ожидание...")
        confidence = st.session_state.get("gesture_confidence", 0.0)

        st.markdown(
            f"""
            <div class="voxx-card" style="text-align: center;">
                <p style="color: #A0A0B2; margin: 0;">Текущий результат</p>
                <h1 style="font-size: 48px; margin: 10px 0;">{last_gesture}</h1>
                <span class="voxx-badge">Уверенность: {int(confidence * 100)}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📚 Справочник жестов")
        for key, g in GESTURE_DICTIONARY.items():
            with st.expander(f"{g.symbol} {g.name} ({g.category})"):
                st.write(f"**Значение:** {g.meaning}")
                st.write(f"**Описание:** {g.description}")
