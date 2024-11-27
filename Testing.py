import streamlit as st
import pyttsx3
import tempfile
import os

# Set up the Streamlit app
st.set_page_config(
    page_title="Realistic Text-to-Speech App",
    page_icon="🔊",
    layout="centered",
)

# Header
st.title("🔊 Realistic Text-to-Speech App")
st.write("Convert your text into speech with customizable voice settings!")

# Sidebar for settings
st.sidebar.header("🎛️ Voice Settings")

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Voice rate setting
rate = st.sidebar.slider("Speech Rate (Words per Minute)", min_value=100, max_value=300, value=150, step=10)
engine.setProperty('rate', rate)

# Volume setting
volume = st.sidebar.slider("Volume", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
engine.setProperty('volume', volume)

# Voice selection
voices = engine.getProperty('voices')
voice_names = [voice.name for voice in voices]
selected_voice = st.sidebar.selectbox("Choose a Voice", options=voice_names)
# Set the selected voice
for voice in voices:
    if voice.name == selected_voice:
        engine.setProperty('voice', voice.id)
        break

# Main input area
text = st.text_area("Enter your text here:", placeholder="Type something...")

if st.button("🔊 Convert to Speech"):
    if text.strip():
        # Convert text to speech
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_filename = temp_audio.name
            engine.save_to_file(text, temp_filename)
            engine.runAndWait()
        
        # Success message
        st.success("Speech conversion successful! 🎉")
        
        # Audio playback
        audio_file = open(temp_filename, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        
        # Download link
        st.download_button(
            label="⬇️ Download Audio",
            data=audio_bytes,
            file_name="speech_output.mp3",
            mime="audio/mp3"
        )
        
        # Clean up
        audio_file.close()
        os.remove(temp_filename)
    else:
        st.error("Please enter some text to convert!")

# Footer
st.markdown(
    """
    ---
    Made with ❤️ using Streamlit and pyttsx3
    """
)
