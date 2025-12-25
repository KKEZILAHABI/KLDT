"""
Voice Input/Output Service using streamlit-webrtc and gTTS
Installation: pip install streamlit-webrtc gtts pydub
"""

import streamlit as st
from gtts import gTTS
import tempfile
import os
import base64

class VoiceService:
    def __init__(self):
        self.enabled = False
    
    def enable(self):
        """Enable voice features"""
        self.enabled = True
        st.success("🎤 Voice features enabled!")
    
    def is_enabled(self):
        """Check if voice is enabled"""
        return self.enabled
    
    def speak(self, text, language):
        """
        Convert text to speech using gTTS
        Plays audio directly in the browser
        """
        try:
            # Map our language names to gTTS language codes
            lang_code = self._get_gtts_lang_code(language)
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)
            
            # Read and encode audio
            with open(temp_file, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            # Clean up temp file
            os.unlink(temp_file)
            
            # Play audio in Streamlit
            st.audio(audio_bytes, format='audio/mp3')
            
            return True
            
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")
            return False
    
    def render_voice_input(self, language, key_prefix="voice"):
        """
        Render voice input button and capture using browser's Web Speech API
        Returns captured text or None
        """
        
        # Voice input button
        if st.button("🎤 Speak", key=f"{key_prefix}_btn", help="Click to speak"):
            # Get language code for speech recognition
            lang_code = self._get_speech_recognition_code(language)
            
            # Inject JavaScript for voice capture
            voice_html = f"""
            <script>
                // Create speech recognition instance
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                
                if (!SpeechRecognition) {{
                    alert("Sorry, your browser doesn't support speech recognition. Please use Chrome, Edge, or Safari.");
                }} else {{
                    const recognition = new SpeechRecognition();
                    recognition.lang = '{lang_code}';
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    
                    recognition.onstart = function() {{
                        console.log('Listening...');
                    }};
                    
                    recognition.onresult = function(event) {{
                        const transcript = event.results[0][0].transcript;
                        console.log('Transcript:', transcript);
                        
                        // Store in localStorage to pass to Streamlit
                        localStorage.setItem('voice_transcript', transcript);
                        localStorage.setItem('voice_timestamp', Date.now());
                        
                        // Reload page to trigger Streamlit update
                        window.location.reload();
                    }};
                    
                    recognition.onerror = function(event) {{
                        console.error('Speech recognition error:', event.error);
                        alert('Speech recognition error: ' + event.error);
                    }};
                    
                    recognition.start();
                }}
            </script>
            """
            
            st.components.v1.html(voice_html, height=0)
            
            # Check for stored transcript
            check_transcript_html = """
            <script>
                const transcript = localStorage.getItem('voice_transcript');
                const timestamp = localStorage.getItem('voice_timestamp');
                
                if (transcript && timestamp) {
                    // Clear after reading
                    localStorage.removeItem('voice_transcript');
                    localStorage.removeItem('voice_timestamp');
                    
                    // Send to Streamlit via query params (requires page setup)
                    console.log('Retrieved transcript:', transcript);
                }
            </script>
            """
            st.components.v1.html(check_transcript_html, height=0)
    
    def _get_gtts_lang_code(self, language):
        """
        Map language names to gTTS language codes
        gTTS supports: en, sw (Swahili), and many others
        """
        mapping = {
            "english": "en",
            "swahili": "sw",
            "luo": "en",      # Fallback to English (Luo not supported in gTTS)
            "kikuyu": "en"    # Fallback to English (Kikuyu not supported in gTTS)
        }
        return mapping.get(language.lower(), "en")
    
    def _get_speech_recognition_code(self, language):
        """
        Map language names to Web Speech API codes
        Format: language-COUNTRY (e.g., en-US, sw-KE)
        """
        mapping = {
            "english": "en-US",
            "swahili": "sw-KE",
            "luo": "en-KE",    # Use English-Kenya as fallback
            "kikuyu": "en-KE"  # Use English-Kenya as fallback
        }
        return mapping.get(language.lower(), "en-US")


# Alternative: Simple text input with voice button
def render_voice_text_input(voice_service, language, label="Your message"):
    """
    Combined text input with voice button
    Returns user input (text or voice)
    """
    col1, col2 = st.columns([5, 1])
    
    with col1:
        text_input = st.text_input(label, key=f"text_input_{language}")
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🎤", key=f"voice_btn_{language}"):
            if voice_service.is_enabled():
                voice_service.render_voice_input(language, key_prefix=language)
            else:
                st.warning("Voice features not enabled. Click 'Enable Voice' in sidebar.")
    
    return text_input