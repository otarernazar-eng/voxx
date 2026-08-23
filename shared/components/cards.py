"""
Card and Banner UI Components
"""
import streamlit as st


def render_feature_card(title: str, description: str, icon: str, page_link: str, badge: str = "Оффлайн"):
    """Render interactive feature card with glassmorphism styling."""
    st.markdown(
        f"""
        <div class="voxx-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <span style="font-size: 36px;">{icon}</span>
                <span class="voxx-badge">{badge}</span>
            </div>
            <h3 style="margin-top: 12px; margin-bottom: 8px;">{title}</h3>
            <p style="color: #A0A0B2; font-size: 14px; margin-bottom: 16px;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(f"Открыть {title}", key=f"btn_nav_{page_link}"):
        st.switch_page(page_link)


def render_info_banner(message: str, type_str: str = "info"):
    """Render accessibility alert banner (info, success, warning, danger)."""
    color_map = {
        "info": "#0984E3",
        "success": "#00B894",
        "warning": "#FDCB6E",
        "danger": "#FF7675"
    }
    border_color = color_map.get(type_str, "#6C5CE7")
    
    st.markdown(
        f"""
        <div style="
            background: rgba(26, 26, 46, 0.9);
            border-left: 6px solid {border_color};
            border-radius: 8px;
            padding: 16px 20px;
            margin: 15px 0;
            color: #F1F1F6;
            font-weight: 500;
        ">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )
