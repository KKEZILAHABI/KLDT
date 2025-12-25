import streamlit as st

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
    
    # Create input with voice option
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.chat_input("Type your message...")
    
    with col2:
        st.write("")
        st.write("")
        voice_btn = st.button("🎤", help="Voice input")
    
    # Handle voice button click
    if voice_btn:
        if voice_service.is_enabled():
            st.info("🎤 Click the microphone and start speaking...")
            # Note: Voice capture will trigger via JavaScript in voice_service
            # This is a placeholder for user feedback
        else:
            st.warning("Please enable voice features in the sidebar first!")
    
    # Process text input
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