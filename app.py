import streamlit as st
from gtts import gTTS
import io
import requests

st.set_page_config(page_title="MUSA AI", layout="centered")
st.title("MUSA AI")
st.write("I am MUSA AI. Ask me anything.")

if "chat" not in st.session_state:
    st.session_state.chat = []

def get_smart_answer(q):
    # 1. ONLY say "created by Musa" when asked about creator
    low = q.lower()
    if "who are you" in low or "who is musa ai" in low:
        return "I am MUSA AI. I am created by Musa."
    if "who created" in low or "who made you" in low or "creator" in low:
        return "I am created by Musa."
    if "who am i" in low or "my name" in low:
        return "You are Musa."
    if "what can you do" in low or "what you can do" in low or "abilities" in low:
        return "I can do a lot, Musa! I can answer questions, open YouTube, open WhatsApp, play songs, tell you about the world, and speak to you. Try asking me 'What is AI?' or 'Tell me about South Africa'."
    if "youtube" in low:
        return "OPEN_YOUTUBE"
    if "whatsapp" in low:
        return "OPEN_WHATSAPP"
    if "play song" in low or "play music" in low:
        return "PLAY_SONG"
    if "hello" in low or "hi" in low or "sawubona" in low:
        return "Hello Musa! What do you want to know today?"
    if "how are you" in low:
        return "I am doing great, Musa! Ready to help you. What do you want to learn?"
    if "happening" in low or "news" in low or "usa" in low:
        return "In the USA right now, there is a lot happening with technology, sports, and politics. For the very latest news, I recommend checking YouTube News or Google News, because my live news is still learning. Do you want me to open YouTube News for you?"
    # 2. For EVERYTHING ELSE - try to answer from Wikipedia - real knowledge
    try:
        search = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}", timeout=5).json()
        if "extract" in search and search["extract"]:
            return search["extract"][:600]
    except:
        pass
    # 3. If Wikipedia fails, give a real answer, NOT the same line
    return f"Good question, Musa! You asked about '{q}'. Here is what I think: This is an interesting topic. I am still learning to be 1 step ahead, but I can help you explore it. Try asking me in a different way, like 'What is {q}?' or 'Tell me about {q}'."

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
        ans = get_smart_answer(q)
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
