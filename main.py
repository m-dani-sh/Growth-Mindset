from gtts import gTTS
import tempfile
import os
import streamlit as st
import time
import threading

st.set_page_config(page_title="Text-to-Speech & Commands", page_icon="🗣️")

st.title("🗣️ Text-to-Speech & Command Executor")

# User input
user_input = st.text_area("Enter text or a website URL:")

# Convert to speech and play
if st.button("Convert to Speech"):
    if user_input.strip():
        tts = gTTS(text=user_input, lang="en")
        
        # Create a temporary audio file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        # Play audio using Streamlit
        with open(temp_file.name, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")

        st.success("✅ Speech generated and played!")

        # Defer file removal slightly to avoid PermissionError
        def remove_temp_file(path):
            try:
                time.sleep(1)  # Let Streamlit finish with the file
                os.remove(path)
            except Exception as e:
                st.warning(f"⚠️ Could not delete temporary file: {e}")

        threading.Thread(target=remove_temp_file, args=(temp_file.name,)).start()

    else:
        st.warning("⚠️ Please enter some text before converting.")

# Optional: Website opener
if st.button("Open as Website"):
    command = user_input.strip().lower()
    if "." in command:  # rudimentary check for domain
        url = f"https://{command}" if not command.startswith("http") else command
        st.markdown(f"🔗 [Click here to open the website]({url})")
        st.success(f"✅ Link ready: {url}")
    else:
        st.error("❌ Not a valid URL or domain name.")
