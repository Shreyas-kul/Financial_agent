import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from gpt4all import GPT4All
from dotenv import load_dotenv
import os
import time
import subprocess
import threading

# Load environment variables
load_dotenv()

def speak_text(text, rate=175):
    """Speak the given text using macOS say command"""
    try:
        # Make sure we have a string
        if not isinstance(text, str):
            text = str(text)
            
        # Adjust the rate (words per minute)
        rate = int(rate * 1.5)  # Convert slider value to appropriate rate
        
        # Create and start the speech process
        process = subprocess.Popen(['say', '-r', str(rate), text])
        
        # Wait for the speech to complete with a timeout
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            st.warning("Speech synthesis took too long and was interrupted")
            
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")

# Initialize the LLM
@st.cache_resource
def init_llm():
    try:
        # Initialize GPT4All with a smaller model
        model = GPT4All("orca-mini-3b-gguf2-q4_0")
        return model
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return None

# Initialize speech recognizer
recognizer = sr.Recognizer()

def record_audio(duration=5):
    """Record audio from microphone for specified duration"""
    sample_rate = 44100
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate, channels=1, dtype='float64')
    st.info(f"Recording for {duration} seconds...")
    sd.wait()
    return recording, sample_rate

def audio_to_text(audio_data, sample_rate):
    """Convert audio data to text using speech recognition"""
    try:
        # Convert numpy array to audio file format
        audio_segment = (audio_data * 32767).astype(np.int16)
        audio = sr.AudioData(audio_segment.tobytes(), sample_rate, 2)
        
        # Perform speech recognition
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        st.error(f"Error in speech recognition: {str(e)}")
        return None

def get_ai_response(llm, prompt):
    """Get response from GPT4All model"""
    try:
        # Get response from model with streaming disabled
        response = llm.generate(
            prompt,
            max_tokens=512,
            temp=0.7,
            top_p=0.95,
            repeat_penalty=1.1,
            top_k=40,
            streaming=False  # Disable streaming to get direct string response
        )
        return response
    except Exception as e:
        st.error(f"Error with GPT4All model: {str(e)}")
        return None

def main():
    st.title("🎙️ Voice & Text AI Assistant (Offline)")
    st.write("Interact with AI using voice or text input! Running on GPT4All")

    # Initialize the LLM
    with st.spinner("Loading AI model..."):
        llm = init_llm()
        if llm is None:
            st.error("Failed to initialize the AI model. Please try again.")
            return

    # Add voice settings
    with st.sidebar:
        st.subheader("Voice Settings")
        voice_enabled = st.checkbox("Enable Voice Response", value=True)
        voice_speed = st.slider("Voice Speed", min_value=100, max_value=250, value=175, step=25)
        
        # Test voice button
        if st.button("Test Voice"):
            if voice_enabled:
                speak_text("Hello! This is a test of the text-to-speech system.", voice_speed)
            else:
                st.error("Voice output is disabled")

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["Voice Input", "Text Input"])

    with tab1:
        st.subheader("Voice Input")
        col1, col2 = st.columns([1, 3])
        with col1:
            duration = st.number_input("Recording duration (seconds)", min_value=1, max_value=10, value=5)
        if st.button("🎤 Start Recording"):
            with st.spinner("Recording..."):
                audio_data, sample_rate = record_audio(duration)
                st.success("Recording completed!")
                
                # Convert speech to text
                text = audio_to_text(audio_data, sample_rate)
                if text:
                    st.info("You said: " + text)
                    
                    # Get AI response
                    with st.spinner("Getting AI response..."):
                        response = get_ai_response(llm, text)
                        if response:
                            st.success("AI Response:")
                            st.write(response)
                            
                            # Speak the response if voice is enabled
                            if voice_enabled:
                                with st.spinner("Speaking response..."):
                                    speak_text(response, voice_speed)

    with tab2:
        st.subheader("Text Input")
        user_input = st.text_area("Enter your message:", height=100)
        if st.button("Send"):
            if user_input:
                with st.spinner("Getting AI response..."):
                    response = get_ai_response(llm, user_input)
                    if response:
                        st.success("AI Response:")
                        st.write(response)
                        
                        # Speak the response if voice is enabled
                        if voice_enabled:
                            with st.spinner("Speaking response..."):
                                speak_text(response, voice_speed)
            else:
                st.warning("Please enter some text!")

if __name__ == "__main__":
    main() 