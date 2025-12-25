import streamlit as st
from frontend.ui_main import render_main_ui
from backend.translation_engine import TranslationEngine
from backend.voice_service import VoiceService
import config.languages as lang_config

def main():
    # Initialize services
    translator = TranslationEngine()
    voice = VoiceService()
    
    # Setup page
    st.set_page_config(
        page_title="Kenyan Translator",
        page_icon="🇰🇪",
        layout="wide"
    )
    
    # Render UI
    render_main_ui(translator, voice)

if __name__ == "__main__":
    main()