import streamlit as st
from gtts import gTTS
from io import BytesIO
import time
import pandas as pd

st.set_page_config(page_title="Deutsche Diktat-Übung", layout="wide")

st.title("Deutsche Diktat-Übung (Englische Wörter auf Papier schreiben)")

st.markdown("""
Klicken Sie auf „Start“, der Computer liest die englischen Wörter nacheinander auf Deutsch vor.  
Nach jedem Wort haben Sie **5 Sekunden** Zeit, um es aufzuschreiben.  
Am Ende sehen Sie alle Wörter in einer Tabelle (Englisch | Deutsch | Chinesisch) –  
**klicken Sie auf ein englisches Wort**, um es auf Deutsch vorgelesen zu hören!
""")

# Wortliste mit Übersetzungen: Englisch | Deutsch | Chinesisch
vocabulary = [
    {"Englisch": "apple",     "Deutsch": "Apfel",     "Chinesisch": "苹果"},
    {"Englisch": "banana",    "Deutsch": "Banane",    "Chinesisch": "香蕉"},
    {"Englisch": "cat",       "Deutsch": "Katze",     "Chinesisch": "猫"},
    {"Englisch": "dog",       "Deutsch": "Hund",      "Chinesisch": "狗"},
    {"Englisch": "elephant",  "Deutsch": "Elefant",   "Chinesisch": "大象"},
    {"Englisch": "flower",    "Deutsch": "Blume",     "Chinesisch": "花"},
    {"Englisch": "house",     "Deutsch": "Haus",      "Chinesisch": "房子"},
    {"Englisch": "icecream",  "Deutsch": "Eiscreme",  "Chinesisch": "冰淇淋"},
    {"Englisch": "jungle",    "Deutsch": "Dschungel", "Chinesisch": "丛林"},
    {"Englisch": "kite",      "Deutsch": "Drachen",   "Chinesisch": "风筝"},
    {"Englisch": "lemon",     "Deutsch": "Zitrone",   "Chinesisch": "柠檬"},
    {"Englisch": "mountain",  "Deutsch": "Berg",      "Chinesisch": "山"},
    {"Englisch": "notebook",  "Deutsch": "Notizbuch", "Chinesisch": "笔记本"},
    {"Englisch": "ocean",     "Deutsch": "Ozean",     "Chinesisch": "海洋"},
    {"Englisch": "pencil",    "Deutsch": "Bleistift", "Chinesisch": "铅笔"},
]

words = [item["Englisch"] for item in vocabulary]  # 只用于朗读的英文单词列表

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.is_running = False

def speak_german(text, slow=False):
    """生成德语发音的音频（内存中）"""
    tts = gTTS(text=text, lang='de', slow=slow)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# 开始按钮
if st.button("Start! 🚀", type="primary"):
    st.session_state.current_index = 0
    st.session_state.is_running = True
    st.rerun()

# 听写过程
if st.session_state.is_running:
    if st.session_state.current_index < len(words):
        idx = st.session_state.current_index
        word = words[idx]

        st.subheader(f"Wort {idx+1} von {len(words)}")
        st.write(f"Lese vor: **{word}** (deutsche Aussprache)")

        audio = speak_german(word)
        st.audio(audio, format="audio/mp3", autoplay=True)

        time.sleep(1.5)
        num_audio = speak_german(f"Das Wort Nummer {idx+1}.", slow=True)
        st.audio(num_audio, format="audio/mp3")

        st.info("**5 Sekunden** Zeit zum Aufschreiben …")
        time.sleep(5)

        st.session_state.current_index += 1
        st.rerun()

    else:
        st.success("Diktat beendet! Sehr gut gemacht! ✨")

        # 结束时显示三列表格
        st.subheader("Alle richtigen Antworten:")

        df = pd.DataFrame(vocabulary)

        # 使 Englisch 列可点击发音（使用 expander + 按钮实现交互）
        for index, row in df.iterrows():
            with st.expander(f"{row['Englisch']}"):
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"**Deutsch:** {row['Deutsch']}")
                col1.markdown(f"**Chinesisch:** {row['Chinesisch']}")
                if col2.button("▶ Anhören (Deutsch)", key=f"play_{index}"):
                    audio = speak_german(row['Englisch'])  # 德语读英文单词
                    st.audio(audio, format="audio/mp3", autoplay=True)

        st.session_state.is_running = False

# 小提示：孩子可以自己添加单词
st.markdown("---")
st.info("Tipp: Bearbeiten Sie die `vocabulary`-Liste im Code, um neue Wörter hinzuzufügen!")