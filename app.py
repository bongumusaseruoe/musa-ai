import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="MUSA AI", layout="centered")
st.title("MUSA AI")
st.write("Ask me anything. I remember what we talked about.")

if "chat" not in st.session_state:
    st.session_state.chat = []
if "pending" not in st.session_state:
    st.session_state.pending = None
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

def speak(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except:
        return None

def answer(q):
    low = q.lower().strip()

    # 1. YES / NO - THIS IS THE BIG FIX - It remembers!
    if low in ["yes", "yes please", "yeah", "ok", "okay", "do it", "open it", "please"]:
        if st.session_state.pending == "youtube":
            st.session_state.pending = None
            return "Opening YouTube now.", "https://www.youtube.com"
        if st.session_state.pending == "whatsapp":
            st.session_state.pending = None
            return "Opening WhatsApp now.", "https://web.whatsapp.com"
        if st.session_state.pending == "song":
            st.session_state.pending = None
            return "Playing a song now.", "https://www.youtube.com/results?search_query=amapiano"
        return "Yes - what do you want me to do? Say 'open YouTube' or 'play song'.", None

    if low in ["no", "no thanks", "not now"]:
        st.session_state.pending = None
        return "Okay, no problem. What else?", None

    # 2. Creator - ONLY time we say the name
    if "who are you" in low:
        return "I am MUSA AI. I am created by Musa.", None
    if "who created" in low or "who made you" in low:
        return "I am created by Musa.", None

    # 3. Commands - Ask permission first, then wait for YES
    if "youtube" in low:
        st.session_state.pending = "youtube"
        return "Do you want me to open YouTube?", None
    if "whatsapp" in low:
        st.session_state.pending = "whatsapp"
        return "Do you want me to open WhatsApp?", None
    if "play song" in low or "play music" in low or "song" in low:
        st.session_state.pending = "song"
        return "Do you want me to play a song?", None

    # 4. Normal questions - FAST, no Wikipedia slow load
    if "what can you do" in low:
        return "I can answer questions, open YouTube, open WhatsApp, and play songs. I also remember what you said. Try 'open YouTube' then say 'yes'.", None
    if "hello" in low or "hi" in low:
        return "Hello! How can I help?", None
    if "how are you" in low:
        return "I am doing well. What do you want to do?", None
    if "happening in usa" in low or "news" in low:
        st.session_state.pending = "youtube"
        return "Do you want me to open YouTube News so you can see what is happening in the USA?", None
    if "what is ai" in low:
        return "AI means Artificial Intelligence. It is a computer program that can learn, answer questions, and help people - like me.", None
    if "what is" in low or "tell me about" in low or "who is" in low:
        topic = q.replace("what is", "").replace("tell me about", "").replace("who is", "").strip()
        return f"{topic} is an interesting topic. I am learning more about it every day. Ask me something else, or say 'open YouTube' to see videos about it.", None

    # 5. Fallback - NEVER repeat same line
    return f"You said: '{q}'. I understand. Can I help you with something else? Try 'open YouTube', 'open WhatsApp', or 'play song'.", None

# Show chat - NO audio for old messages = FAST
for m in st.session_state.chat:
    st.write(f"**You:** {m['text']}" if m['who']=='you' else f"**MUSA AI:** {m['text']}")

# Only play LAST audio
if st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3")

# Quick Yes / No buttons - when it asks permission
if st.session_state.pending:
    st.write("MUSA AI is asking permission:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ YES, DO IT"):
            ans, link = answer("yes")
            st.session_state.chat.append({"who":"you","text":"Yes"})
            st.session_state.chat.append({"who":"ai","text":ans})
            st.session_state.last_audio = speak(ans)
            if link:
                st.link_button("Click to Open", link)
            st.rerun()
    with c2:
        if st.button("❌ NO"):
            ans, _ = answer("no")
            st.session_state.chat.append({"who":"you","text":"No"})
            st.session_state.chat.append({"who":"ai","text":ans})
            st.session_state.last_audio = speak(ans)
            st.rerun()

q = st.text_input("Ask MUSA AI anything...")
if st.button("Ask MUSA AI"):
    if q:
        ans, link = answer(q)
        st.session_state.chat.append({"who":"you","text":q})
        st.session_state.chat.append({"who":"ai","text":ans})
        st.session_state.last_audio = speak(ans)
        if link:
            st.link_button("Click to Open", link)
        st.rerun()
