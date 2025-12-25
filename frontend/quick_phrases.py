import streamlit as st
from backend.phrase_database import PhraseDatabase

def render_quick_phrases(translator, source_lang, target_lang):
    """Display quick phrase buttons"""
    st.subheader("Quick Phrases")
    
    # Load phrase database
    phrase_db = PhraseDatabase()
    categories = phrase_db.get_categories()
    
    # Select category
    category = st.selectbox("Category:", categories)
    
    # Get phrases for selected category
    phrases = phrase_db.get_phrases_by_category(category)
    
    # Display phrase buttons
    for phrase in phrases:
        if phrase.get(source_lang):  # Check if phrase exists in source language
            phrase_text = phrase[source_lang]
            if st.button(phrase_text, key=f"phrase_{phrase_text}"):
                # Get translation for this phrase
                translation = phrase.get(target_lang, "Translation not available")
                
                # Add to chat
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                
                st.session_state.messages.append({
                    "role": "user",
                    "content": phrase_text
                })
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"In {target_lang}:",
                    "translation": translation
                })
                
                st.rerun()