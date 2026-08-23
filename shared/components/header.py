"""
Header Component for VoxX App
Renders accessible header banner and top controls.
"""
import streamlit as st
from voxx.core.config import APP_NAME, APP_SLOGAN


def render_app_header(title_suffix: str = "", icon: str = "🤟"):
    """Render top application header with quick accessibility controls."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                <span style="font-size: 42px;">{icon}</span>
                <div>
                    <h1 style="margin: 0; padding: 0; font-size: 32px;">{APP_NAME} {title_suffix}</h1>
                    <p style="margin: 0; color: #A0A0B2; font-size: 15px;">{APP_SLOGAN}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        # Quick accessibility toggles in sidebar header or top right
        high_contrast = st.session_state.get("high_contrast", False)
        hc_label = "👁️‍🗨️ Обычный" if high_contrast else "👁️‍🗨️ Контраст"
        if st.button(hc_label, key=f"quick_hc_toggle_{icon}"):
            st.session_state.high_contrast = not high_contrast
            st.rerun()

    st.markdown("---")
