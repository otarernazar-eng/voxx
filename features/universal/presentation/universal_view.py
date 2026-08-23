"""
Presentation layer for Universal Communication (AAC & SOS matrix)
"""
import streamlit as st
from features.universal.domain.quick_communicator import QuickCommunicator
from shared.services.tts_service import TTSService
from core.utils import trigger_haptic_feedback


def render_universal_screen():
    """Render universal communicator matrix with large AAC phrase buttons."""
    st.markdown("## 💬 Универсальный Коммуникатор (AAC)")
    st.markdown(
        "Быстрый набор фраз крупными визуальными кнопками для людей с нарушениями речи "
        "и кнопка мгновенного вызова помощи SOS."
    )

    communicator = QuickCommunicator()
    tts = TTSService()

    # Emergency SOS Banner
    st.markdown("### 🚨 Сигнал Тревоги")
    if st.button("🆘 МГНОВЕННЫЙ СИГНАЛ SOS / ВЫЗОВ ПОМОЩИ", key="btn_sos_main", type="primary"):
        st.session_state.emergency_sos_active = True
        trigger_haptic_feedback()
        tts.speak("Внимание! Требуется срочная помощь!")

    if st.session_state.get("emergency_sos_active", False):
        st.error("🚨 СИГНАЛ ТРЕВОГИ АКТИВИРОВАН! Голосовое оповещение и вибросигнал запущены.")
        if st.button("⏹️ Сбросить сигнал SOS", key="btn_reset_sos"):
            st.session_state.emergency_sos_active = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🗣️ Карточки Быстрых Фраз")

    categories = ["Все", "Базовые", "Здоровье", "Навигация", "Общение", "Покупки"]
    selected_cat = st.selectbox("Категория фраз:", categories, key="aac_cat_select")

    phrases = communicator.get_phrases_by_category(selected_cat)

    cols = st.columns(3)
    for idx, p in enumerate(phrases):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="voxx-card" style="text-align: center; border-left: 6px solid {p.bg_color};">
                    <span style="font-size: 40px;">{p.icon}</span>
                    <h3 style="font-size: 18px; margin: 10px 0;">{p.text}</h3>
                    <span class="voxx-badge">{p.category}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"🔊 Произнести: {p.text}", key=f"btn_phrase_{p.id}"):
                st.session_state.last_spoken_phrase = p.text
                tts.speak(p.text)
                trigger_haptic_feedback()

    # Add custom phrase option
    st.markdown("---")
    st.markdown("### ➕ Добавить свою быструю фразу")
    new_phrase = st.text_input("Введите новую фразу:", placeholder="Мне нужно лекарство...", key="new_aac_input")
    if st.button("Сохранить фразу", key="btn_save_aac"):
        if new_phrase:
            st.session_state.custom_quick_phrases.append(new_phrase)
            st.success(f"Фраза '{new_phrase}' добавлена в меню!")
