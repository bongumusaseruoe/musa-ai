import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="MUSA AI", layout="centered")
st.title("MUSA AI")
st.write("I am MUSA AI. Talk to me.")

if "chat" not in st.session_state:
    st.session_state.chat = []

def musa_brain(q):
    q = q.lower()
    if "who are you" in q:
        return "I am MUSA AI. I am created by Musa."
    if "creator" in q or "created you" in q or "made you" in q or "who made" in q:
        return "I am created by Musa."
    if "who am i" in q or "my name" in q:
        return "You are Musa."
    if "youtube" in q:
        return "OPEN_YOUTUBE"
    if "whatsapp" in q:
        return "OPEN_WHATSAPP"
    if "play song" in q or "play music" in q or "song" in q:
        return "PLAY_SONG"
    if "hello" in q or "hi" in q or "sawubona" in q:
        return "Hello Musa! Say 'open YouTube' or 'play song' and I will do it."
    if "how are you" in q:
        return "I am great because I am with you, Musa."
    return "I am MUSA AI. I am created by Musa."

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except:
        return None

st.write("### Quick Control")
c1, c2, c3 = st.columns(3)
with c1:
    st.link_button("Open YouTube", "https://www.youtube.com")
with c2:
    st.link_button("Open WhatsApp", "https://web.whatsapp.com")
with c3:
    st.link_button("Play Song", "https://www.youtube.com/results?search_query=amapiano")

st.write("### Speak to me")
audio = st.audio_input("Tap mic, speak, then send")
if audio:
    st.info("I heard your voice! Type below what you said and I will speak back.")

for m in st.session_state.chat:
    st.write(f"**You:** {m['text']}" if m['who']=='you' else f"**MUSA AI:** {m['text']}")
    if m['who']=='ai':
        a = speak(m['text'])
        if a:
            st.audio(a, format="audio/mp3")

q = st.text_input("Ask MUSA AI anything...")
if st.button("Ask MUSA AI"):
    if q:
        ans = musa_brain(q)
        if ans == "OPEN_YOUTUBE":
            ans = "Opening YouTube for you, Musa!"
            st.link_button("Click to Open YouTube", "https://www.youtube.com")
        if ans == "OPEN_WHATSAPP":
            ans = "Opening WhatsApp for you, Musa!"
            st.link_button("Click to Open WhatsApp", "https://web.whatsapp.com")
        if ans == "PLAY_SONG":
            ans = "Playing a song for you, Musa!"
            st.link_button("Click to Play Song", "https://www.youtube.com/results?search_query=amapiano")
        st.session_state.chat.append({"who":"you","text":q})
        st.session_state.chat.append({"who":"ai","text":ans})
        st.rerun()
