import streamlit as st
from gtts import gTTS
from io import BytesIO
import time

st.set_page_config(page_title="德语听写英语单词", layout="centered")

st.title("德语听写练习（纸上写答案版）")
st.markdown("点击「开始听写」，电脑会用德语一个个读英语单词。每个词后暂停5秒写在纸上，最后显示答案。")

# 单词列表（孩子自己改最有意思！）
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

if st.button("开始听写！🚀", type="primary"):
    st.session_state.current_index = 0
    st.session_state.is_running = True
    st.rerun()

if st.session_state.is_running:
    if st.session_state.current_index < len(words):
        idx = st.session_state.current_index
        word = words[idx]

        st.subheader(f"第 {idx+1} 个单词（共 {len(words)} 个）")
        st.write(f"正在朗读：**{word}**（德语发音）")

        audio = speak_german(word)
        st.audio(audio, format="audio/mp3", autoplay=True)

        time.sleep(1.5)  # 短暂间隔，避免声音重叠
        num_audio = speak_german(f"Das Wort Nummer {idx+1}.", slow=True)
        st.audio(num_audio, format="audio/mp3")

        st.info(f"你有 **5秒** 时间写下来……")
        time.sleep(5)

        st.session_state.current_index += 1
        st.rerun()  # 自动下一题

    else:
        st.success("听写结束！超级棒✨")
        st.subheader("全部正确答案：")
        for i, w in enumerate(words, 1):
            st.write(f"{i:2d}. **{w}**")

        st.session_state.is_running = False