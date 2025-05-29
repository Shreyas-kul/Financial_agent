import streamlit as st
import requests
from datetime import datetime
import pytz
import sys
import os
from typing import List

# Add parent directory to Python path
try:
    from orchestrator.crew_manager import FinancialCrew
except ImportError:
    # Try alternative import path for Streamlit Cloud
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from orchestrator.crew_manager import FinancialCrew

# Initialize voice features if available
VOICE_ENABLED = False
try:
    import speech_recognition as sr
    import sounddevice as sd
    import numpy as np
    import whisper
    import subprocess
    VOICE_ENABLED = True
except ImportError:
    pass

# Initialize Whisper model if voice is enabled
@st.cache_resource
def load_whisper_model():
    if VOICE_ENABLED:
        return whisper.load_model("base")
    return None

def speak_text(text, rate=175):
    """Speak the given text using macOS say command"""
    if not VOICE_ENABLED:
        st.warning("Voice output is not available. Install voice dependencies to enable this feature.")
        return
        
    try:
        if not isinstance(text, str):
            text = str(text)
        rate = int(rate * 1.5)
        process = subprocess.Popen(['say', '-r', str(rate), text])
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            st.warning("Speech synthesis took too long and was interrupted")
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")

def record_audio(duration=5):
    """Record audio from microphone"""
    if not VOICE_ENABLED:
        st.error("Voice input is not available. Install voice dependencies to enable this feature.")
        return None, None
        
    sample_rate = 44100
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate, channels=1, dtype='float64')
    st.info(f"Recording for {duration} seconds...")
    sd.wait()
    return recording.flatten().tolist(), sample_rate

def process_audio(audio_data, sample_rate):
    """Process audio using Whisper and CrewAI"""
    if not VOICE_ENABLED:
        return None, None
        
    try:
        # Convert audio to numpy array
        audio_array = np.array(audio_data)
        
        # Transcribe audio
        model = load_whisper_model()
        result = model.transcribe(audio_array)
        transcribed_text = result["text"]
        
        # Process with CrewAI
        crew = FinancialCrew()
        response = crew.run_crew()
        
        return transcribed_text, response
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None, None

def process_text(text):
    """Process text using CrewAI"""
    try:
        crew = FinancialCrew()
        response = crew.run_crew()
        return response
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        return None

def main():
    st.title("🎙️ AI Market Brief Assistant")
    st.write("Get your morning market brief with voice interaction!")

    # Sidebar settings
    with st.sidebar:
        st.subheader("Voice Settings")
        if VOICE_ENABLED:
            voice_enabled = st.checkbox("Enable Voice Response", value=True)
            voice_speed = st.slider("Voice Speed", min_value=100, max_value=250, value=175, step=25)
            
            if st.button("Test Voice"):
                if voice_enabled:
                    speak_text("Hello! I'm your AI Market Brief Assistant.", voice_speed)
                else:
                    st.error("Voice output is disabled")
        else:
            st.warning("Voice features are not available. Install the required dependencies to enable voice interaction.")

    # Display current time in different time zones
    col1, col2, col3 = st.columns(3)
    now = datetime.now()
    with col1:
        st.write("New York:", now.astimezone(pytz.timezone('America/New_York')).strftime("%H:%M"))
    with col2:
        st.write("London:", now.astimezone(pytz.timezone('Europe/London')).strftime("%H:%M"))
    with col3:
        st.write("Tokyo:", now.astimezone(pytz.timezone('Asia/Tokyo')).strftime("%H:%M"))

    # Create tabs for different input methods
    if VOICE_ENABLED:
        tab1, tab2 = st.tabs(["Voice Input", "Text Input"])
        
        with tab1:
            st.subheader("Voice Input")
            col1, col2 = st.columns([1, 3])
            with col1:
                duration = st.number_input("Recording duration (seconds)", min_value=1, max_value=10, value=5)
            
            if st.button("🎤 Start Recording"):
                audio_data, sample_rate = record_audio(duration)
                if audio_data and sample_rate:
                    transcribed_text, response = process_audio(audio_data, sample_rate)
                    
                    if transcribed_text and response:
                        st.info(f"You said: {transcribed_text}")
                        st.success("AI Response:")
                        st.write(response)
                        
                        if voice_enabled:
                            speak_text(response, voice_speed)
    else:
        tab2 = st.empty()

    # Text input tab (always available)
    if VOICE_ENABLED:
        with tab2:
            st.subheader("Text Input")
    else:
        st.subheader("Text Input")
        
    user_input = st.text_area("Enter your question:", height=100,
                             placeholder="e.g., What's our risk exposure in Asia tech stocks today, and highlight any earnings surprises?")
    
    if st.button("Send"):
        if user_input:
            response = process_text(user_input)
            if response:
                st.success("AI Response:")
                st.write(response)
                
                if VOICE_ENABLED and voice_enabled:
                    speak_text(response, voice_speed)
        else:
            st.warning("Please enter some text!")

if __name__ == "__main__":
    main() 