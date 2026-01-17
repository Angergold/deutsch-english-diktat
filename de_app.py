import streamlit as st
from gtts import gTTS
from io import BytesIO
import time

st.set_page_config(page_title="Deutsche Diktat-Übung", layout="centered")

st.title("Deutsche Diktat-Übung (Englische Wörter auf Papier schreiben)")

st.markdown("""
Klicken Sie auf „Start“, der Computer liest die englischen Wörter nacheinander auf Deutsch vor.  
Nach jedem Wort haben Sie **5 Sekunden** Zeit, um es aufzuschreiben. Am Ende erscheinen alle richtigen Antworten.
""")

# Wortliste (Kinder können sie selbst ändern!)
words = [
    "apple", "banana", "cat", "dog", "elephant",
    "flower", "house", "icecream", "jungle", "kite",
    "lemon", "mountain", "notebook", "ocean", "pencil"
]

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.is_running = False

def speak_german(text, slow=False):
    tts = gTTS(text=text, lang='de', slow=slow)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

if st.button("Start! 🚀", type="primary"):
    st.session_state.current_index = 0
    st.session_state.is_running = True
    st.rerun()

if st.session_state.is_running:
    if st.session_state.current_index < len(words):
        idx = st.session_state.current_index
        word = words[idx]

        st.subheader(f"Wort {idx+1} von {len(words)}")
        st.write(f"Lese vor: **{word}** (deutsche Aussprache)")

        audio = speak_german(word)
        st.audio(audio, format="audio/mp3", autoplay=True)

        time.sleep(1.5)  # Kurze Pause, damit die Stimmen nicht überlappen
        num_audio = speak_german(f"Das Wort Nummer {idx+1}.", slow=True)
        st.audio(num_audio, format="audio/mp3")

        st.info("**5 Sekunden** Zeit zum Aufschreiben …")
        time.sleep(5)

        st.session_state.current_index += 1
        st.rerun()  # Automatisch zum nächsten Wort

    else:
        st.success("Diktat beendet! Sehr gut gemacht! ✨")
        st.subheader("Alle richtigen Antworten:")
        for i, w in enumerate(words, 1):
            st.write(f"{i:2d}. **{w}**")

        st.session_state.is_running = False