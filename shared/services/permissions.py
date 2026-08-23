"""
Browser Permissions Explanation & WebRTC Fallback Helper Service
"""
import streamlit as st


def render_permission_explanation(force_show: bool = False):
    """
    Renders prominent accessibility card explaining browser camera and microphone permissions.
    Saves dismiss status in st.session_state.
    """
    if not force_show and st.session_state.get("permissions_prompt_dismissed", False):
        return

    st.markdown(
        """
        <div style="
            background-color: #121212;
            border: 4px solid #FFD700;
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 25px;
            color: #FFFFFF;
            box-shadow: 0 8px 30px rgba(255, 215, 0, 0.25);
        " role="region" aria-label="Инструкция по разрешениям браузера">
            <h2 style="color: #FFD700; font-size: 30px; margin-top: 0; display: flex; align-items: center; gap: 12px;">
                📷 🎙️ Запрос разрешений браузера
            </h2>
            <p style="font-size: 18px; line-height: 1.5; color: #FFFFFF;">
                Для полной автономной работы приложения <strong>VoxX</strong> вашему браузеру потребуется доступ к 
                камере и микрофону.
            </p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div style="background: #1E1E1E; border-left: 5px solid #00CEC9; padding: 16px; border-radius: 12px;">
                    <h3 style="color: #00CEC9; margin: 0 0 8px 0; font-size: 20px;">📷 Веб-Камера</h3>
                    <p style="margin: 0; font-size: 15px; color: #E0E0E0;">
                        Нужна для <strong>распознавания жестового языка</strong> в реальном времени (MediaPipe) и 
                        сканирования текста на фотографиях (OCR).
                    </p>
                </div>
                <div style="background: #1E1E1E; border-left: 5px solid #FF7675; padding: 16px; border-radius: 12px;">
                    <h3 style="color: #FF7675; margin: 0 0 8px 0; font-size: 20px;">🎙️ Микрофон</h3>
                    <p style="margin: 0; font-size: 15px; color: #E0E0E0;">
                        Необходим для <strong>преобразования речи в субтитры</strong> (Speech-to-Text) и 
                        определения опасного уровня шумов в помещении.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("📖 Как разрешить доступ в вашем браузере (Chrome / Firefox / Edge / Safari)"):
        st.markdown(
            """
            * **Google Chrome / Yandex / Opera:** Нажмите на иконку замочка или настроек слева от URL-адреса сайта ➔ **Настройки сайтов** ➔ Разрешить **Камеру** и **Микрофон**.
            * **Mozilla Firefox:** Нажмите на значок значка блокировки слева в строке адреса ➔ Удалите заблокированное разрешение ➔ Обновите страницу.
            * **Microsoft Edge:** Нажмите значок замка ➔ **Разрешения для этого сайта** ➔ Установите «Разрешить» для Камеры и Микрофона.
            * **Apple Safari:** Меню Safari ➔ **Настройки для этого веб-сайта** ➔ Камера и Микрофон ➔ **Разрешить**.
            """
        )

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("✅ Я уже разрешил доступ — продолжить", key="btn_dismiss_permissions", use_container_width=True):
            st.session_state["permissions_prompt_dismissed"] = True
            st.rerun()
    with col2:
        if st.button("🔄 Проверить доступ снова", key="btn_retry_permissions", use_container_width=True):
            st.rerun()

    st.markdown("---")


def render_webrtc_permission_error():
    """Renders user-friendly message when WebRTC fails due to denied media permissions."""
    st.error(
        "⚠️ **Доступ к камере или микрофону заблокирован браузером.**\n\n"
        "Пожалуйста, предоставьте доступ в настройках вашего браузера (иконка замка в адресной строке) "
        "и нажмите кнопку ниже."
    )
    if st.button("🔄 Повторить попытку подключения", key="btn_webrtc_retry"):
        st.rerun()
