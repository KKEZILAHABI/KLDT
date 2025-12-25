import streamlit as st
from frontend.chat_interface import render_chat
from frontend.language_selector import render_language_selector
from frontend.quick_phrases import render_quick_phrases

def render_main_ui(translator, voice_service):
    """Main UI layout"""
    st.title("🇰🇪 Kenyan Local Dialect Translator")
    st.caption("Chat-based translation between English, Swahili, Luo & Kikuyu")
    
    # Sidebar for language selection
    with st.sidebar:
        st.header("Settings")
        source_lang, target_lang = render_language_selector()
        
        st.divider()
        render_quick_phrases(translator, source_lang, target_lang)
        
        st.divider()
        if st.button("🗣️ Enable Voice", help="Enable microphone input"):
            voice_service.enable()
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
    
    # Main chat area
    render_chat(translator, source_lang, target_lang, voice_service)