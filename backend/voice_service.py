"""
Voice Input/Output Service using Backend Recording and Speech Recognition
"""

import streamlit as st
from gtts import gTTS
import tempfile
import os
import speech_recognition as sr
from io import BytesIO

class VoiceService:
    def __init__(self):
        # Initialize session state for voice
        if "voice_enabled" not in st.session_state:
            st.session_state.voice_enabled = False
        if "voice_transcript" not in st.session_state:
            st.session_state.voice_transcript = None
        if "voice_audio_processed" not in st.session_state:
            st.session_state.voice_audio_processed = None
        if "recognizer" not in st.session_state:
            # Initialize speech recognizer once
            st.session_state.recognizer = sr.Recognizer()
    
    def enable(self):
        """Enable voice features"""
        st.session_state.voice_enabled = True
        st.success("🎤 Voice features enabled!")
    
    def disable(self):
        """Disable voice features"""
        st.session_state.voice_enabled = False
        st.info("🔇 Voice features disabled")
    
    def is_enabled(self):
        """Check if voice is enabled"""
        return st.session_state.voice_enabled
    
    def speak(self, text, language):
        """
        Convert text to speech using gTTS
        Plays audio directly in the browser
        """
        try:
            if not text or not text.strip():
                return False
                
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
            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            
            return True
            
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")
            return False
    
    def transcribe_audio(self, audio_file, language="english"):
        """
        Transcribe audio file to text using backend speech recognition
        Streamlit's audio_input returns an UploadedFile object
        """
        try:
            recognizer = st.session_state.recognizer
            
            # audio_file is an UploadedFile object, need to read bytes from it
            if hasattr(audio_file, 'read'):
                # It's an UploadedFile, read the bytes
                audio_bytes = audio_file.read()
            else:
                # It's already bytes
                audio_bytes = audio_file
            
            # Create a temporary file to store the audio
            # speech_recognition needs a file-like object or file path
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name
            
            try:
                # Use the audio file with speech_recognition
                with sr.AudioFile(tmp_path) as source:
                    # Adjust for ambient noise (optional, can be slow)
                    # recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Record the audio
                    audio_data = recognizer.record(source)
                
                # Get language code for recognition
                lang_code = self._get_speech_recognition_code(language)
                
                # Recognize speech using Google's API (free, requires internet)
                try:
                    text = recognizer.recognize_google(audio_data, language=lang_code)
                    return text
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    return None
                except sr.RequestError as e:
                    # API unavailable - could fallback to offline recognition
                    st.warning(f"Speech recognition API error: {e}. Please check your internet connection.")
                    return None
            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            
        except Exception as e:
            st.error(f"Speech recognition error: {e}")
            return None
    
    def render_voice_recorder(self, language):
        """
        Render voice recorder using Streamlit's audio_input widget
        This uses backend recording - audio is captured in browser and sent to backend
        """
        if not self.is_enabled():
            return None
        
        st.write("🎤 **Voice Input**")
        audio_file = st.audio_input("Click to record", key="voice_recorder")
        
        if audio_file is not None:
            # Get bytes for hashing (UploadedFile can be read multiple times)
            # Read bytes to create a hash for tracking processed files
            audio_file.seek(0)  # Reset to beginning
            audio_bytes = audio_file.read()
            audio_hash = hash(audio_bytes)
            audio_file.seek(0)  # Reset again for transcription
            
            # Check if we've already processed this audio (avoid reprocessing on reruns)
            if st.session_state.voice_audio_processed != audio_hash:
                # Mark this audio as processed
                st.session_state.voice_audio_processed = audio_hash
                
                # Show processing message
                with st.spinner("🎤 Processing audio..."):
                    # Transcribe the audio (pass the file object)
                    transcript = self.transcribe_audio(audio_file, language)
                    
                    if transcript:
                        # Store transcript in session state for processing
                        st.session_state.voice_transcript = transcript
                        st.success(f"🎤 **Captured:** {transcript}")
                        # Return transcript so it can be used immediately
                        return transcript
                    else:
                        st.warning("⚠️ Could not understand audio. Please try again.")
        
        return None
    
    def get_transcript(self):
        """Get and clear the stored transcript"""
        if st.session_state.voice_transcript:
            transcript = st.session_state.voice_transcript
            st.session_state.voice_transcript = None
            return transcript
        return None
    
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
        Map language names to Speech Recognition API codes
        Format: language-COUNTRY (e.g., en-US, sw-KE)
        """
        mapping = {
            "english": "en-US",
            "swahili": "sw-KE",
            "luo": "en-KE",    # Use English-Kenya as fallback
            "kikuyu": "en-KE"  # Use English-Kenya as fallback
        }
        return mapping.get(language.lower(), "en-US")
