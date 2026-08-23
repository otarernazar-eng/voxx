"""
VoxX Dynamic Accessibility Theme & High-Contrast CSS Injector
"""
import streamlit as st


def apply_custom_css():
    """Inject dynamic CSS tailored for accessibility, font scaling, and high contrast."""
    high_contrast = st.session_state.get("high_contrast", True)
    font_scale = float(st.session_state.get("font_size_scale", 1.0))
    screenreader_mode = st.session_state.get("screenreader_mode", False)

    # Dynamic Typography Calculations (Base 16px scaled up to 32px max)
    base_font_px = int(18 * font_scale)
    h1_px = int(36 * font_scale)
    h2_px = int(28 * font_scale)
    h3_px = int(22 * font_scale)
    btn_font_px = int(20 * font_scale)

    if high_contrast:
        bg_color = "#000000"
        surface_color = "#121212"
        border_color = "#FFD700"
        text_color = "#FFFFFF"
        accent_color = "#FFD700"
        accent_text = "#000000"
    else:
        bg_color = "#0F0F1A"
        surface_color = "#1A1A2E"
        border_color = "#6C5CE7"
        text_color = "#F1F1F6"
        accent_color = "#6C5CE7"
        accent_text = "#FFFFFF"

    custom_css = f"""
    <style>
    /* Global Background & Accessibility Sizing */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-size: {base_font_px}px !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}

    /* Dynamic Headings */
    h1 {{
        font-size: {h1_px}px !important;
        color: {accent_color} !important;
        font-weight: 900 !important;
    }}
    h2 {{
        font-size: {h2_px}px !important;
        color: {text_color} !important;
        font-weight: 700 !important;
    }}
    h3 {{
        font-size: {h3_px}px !important;
        color: {text_color} !important;
    }}

    /* Global Large Button Styles */
    .stButton > button {{
        background-color: {surface_color} !important;
        color: {text_color} !important;
        font-size: {btn_font_px}px !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        border: 3px solid {border_color} !important;
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 12px !important;
    }}

    .stButton > button:hover, .stButton > button:focus {{
        background-color: {accent_color} !important;
        color: {accent_text} !important;
        border-color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        outline: 4px solid #FFFFFF !important;
    }}

    /* Form inputs scaling */
    div[data-baseweb="input"] input, div[data-baseweb="select"] div {{
        font-size: {base_font_px}px !important;
        background-color: {surface_color} !important;
        color: {text_color} !important;
        border-radius: 12px !important;
    }}

    /* Sidebar Navigation Sizing & Active Item Highlight */
    section[data-testid="stSidebar"] {{
        background-color: {surface_color} !important;
        border-right: 3px solid {border_color} !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul {{
        padding-top: 15px !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
        font-size: {int(19 * font_scale)}px !important;
        font-weight: 700 !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
        color: {text_color} !important;
        border: 2px solid transparent !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
        background-color: {accent_color} !important;
        color: {accent_text} !important;
        border-color: #FFFFFF !important;
    }}

    /* Active Page Highlight in Sidebar */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background-color: {accent_color} !important;
        color: {accent_text} !important;
        border: 3px solid #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4) !important;
    }}

    /* Screenreader High Visibility Mode Adjustments */
    {"* { font-weight: 900 !important; letter-spacing: 0.5px !important; }" if screenreader_mode else ""}

    /* Hide standard Streamlit header & footer */
    #MainMenu, footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

