import streamlit as st
import config.languages as langs

def render_language_selector():
    """Render language dropdowns"""
    st.subheader("Languages")
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox(
            "Translate from:",
            options=langs.SUPPORTED_LANGUAGES.keys(),
            format_func=lambda x: langs.SUPPORTED_LANGUAGES[x]["name"],
            key="source_lang"
        )
    
    with col2:
        target_lang = st.selectbox(
            "Translate to:",
            options=langs.SUPPORTED_LANGUAGES.keys(),
            format_func=lambda x: langs.SUPPORTED_LANGUAGES[x]["name"],
            index=2,  # Default to Luo
            key="target_lang"
        )
    
    return source_lang, target_lang