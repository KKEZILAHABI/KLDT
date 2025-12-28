# Voice Input/Output Integration and Mic Icon Placement

## Tasks
- [x] Modify frontend/chat_interface.py to replace st.chat_input() with custom HTML input containing mic icon
- [x] Integrate mic icon click to trigger voice recording start
- [x] Remove separate voice recorder section above chat input
- [x] Test voice input/output functionality
- [x] Verify mic icon is inside input area and functional

# Add Send Button to Chat Input Area

## Tasks
- [x] Update input_html: Adjust input padding (right: 100px), add send button with ➤ icon positioned at right: 60px, styled like mic button (background: none, border: none, cursor: pointer, color: #666; title="Send message")
- [x] Update JavaScript: Add event listener for send button click - if input.value.trim() not empty, submit via ?inputSubmitted=... URL param; optionally, change icon color when input has text
- [x] Verify mic button remains at right: 10px and functional
- [x] Test: Rerun app, type message, click send (triggers translation), confirm Enter key and mic work unchanged

# Implement Voice Recording with UX Indicators and Auto-Submit

## Tasks
- [x] backend/voice_service.py: Implement render_voice_recorder - Custom HTML/JS using SpeechRecognition API, lang from _get_speech_recognition_code; visuals: "🎤 Recording... Speak now!" label, pulsing mic (CSS animation), toggle stop button if needed; on start (when voice_recording=True): init/start recognition; on result/end: set transcript, dispatch 'voiceTranscriptReady', auto-call submitInput() for translation if not empty; on error: show message, stop.
- [x] backend/voice_service.py: Add query param handling after component: if "voiceTranscript" in st.query_params, set st.session_state.voice_transcript = ..., del, rerun; if "voiceRecordingStopped", set voice_recording=False, voice_action="idle", rerun.
- [x] frontend/chat_interface.py: Ensure JS in custom input handles 'voiceTranscriptReady' to populate input and enable send (already does); since auto-submit, no manual needed for voice.
- [x] Test: Rerun app, enable voice, click mic → recording UI shows (pulsing, label), speak (e.g., "Hello"), recognition ends → auto-populates input, submits, translates, displays assistant message with 🔊 Play; confirm text input/send still works; test lang switching.
