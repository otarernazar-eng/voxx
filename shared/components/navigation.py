"""
Navigation helper component for quick links and status bar
"""
import streamlit as st
from core.config import NAV_ITEMS


def render_quick_nav():
    """Render horizontal quick-navigation toolbar."""
    st.markdown("### 🚀 Быстрый переход")
    cols = st.columns(len(NAV_ITEMS))
    
    for idx, (key, item) in enumerate(NAV_ITEMS.items()):
        with cols[idx]:
            if st.button(f"{item['icon']}\n{item['title']}", key=f"quick_nav_{key}"):
                st.switch_page(item["route"])
