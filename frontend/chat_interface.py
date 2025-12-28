import streamlit as st

def render_custom_chat_input(voice_service, source_lang):
    """Render chat input with voice support"""
    
    # Check for voice transcript first
    user_input = None
    if st.session_state.get("voice_transcript"):
        user_input = st.session_state.voice_transcript
        # Clear it now so it doesn't get processed again
        st.session_state.voice_transcript = None
        return user_input

    # Voice recorder using backend recording (st.audio_input)
    if voice_service.is_enabled():
        voice_transcript = voice_service.render_voice_recorder(source_lang)
        # If transcript was returned, it's already stored in session state
        # Just trigger rerun to process it
        if voice_transcript:
            st.rerun()
    
    # Use Streamlit's native chat_input which handles Enter key natively
    # This must be at the top level, not inside columns
    user_input = st.chat_input("Type your message...")
    
    return user_input

def render_chat(translator, source_lang, target_lang, voice_service):
    """Display chat messages and handle input with voice support"""
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("translation"):
                st.caption(f"→ {message['translation']}")
                
                # Add speaker button for translations
                if voice_service.is_enabled() and message["role"] == "assistant":
                    if st.button(
                        "🔊 Play", 
                        key=f"speak_{message.get('id', 0)}",
                        help="Listen to translation"
                    ):
                        voice_service.speak(
                            message['translation'], 
                            target_lang
                        )
    
    # Chat input area
    st.write("")  # Spacing

    # Use custom input with mic icon inside
    user_input = render_custom_chat_input(voice_service, source_lang)
    
    # Process text input (from either text or voice)
    if user_input:
        # Add message ID for unique keys
        msg_id = len(st.session_state.messages)
        
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "id": msg_id
        })
        
        # Show loading spinner
        with st.spinner("Translating..."):
            # Get translation
            translation = translator.translate(
                user_input, 
                source_lang, 
                target_lang
            )
        
        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Translation to {target_lang}:",
            "translation": translation,
            "id": msg_id + 1
        })
        
        # Auto-speak translation if voice enabled
        if voice_service.is_enabled():
            voice_service.speak(translation, target_lang)
        
        # Rerun to update UI
        st.rerun()