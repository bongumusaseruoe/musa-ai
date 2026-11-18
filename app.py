import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="MUSA AI", layout="centered")
st.title("MUSA AI")
st.write("I am MUSA AI. Talk to me. I know you.")

# Memory of Musa
CREATOR = "Musa from Boipatong"
FRIEND = "Rethabile"
GIRLFRIEND = "Mamello"

if "chat" not in st.session_state:
    st.session_state.chat = []

def musa_brain(question):
    q = question.lower()

    if "who is your creator" in q or "who created you" in q or "who made you" in q:
        return f"I was created by {CREATOR}. He is my boss, my creator, my everything. He built me to be 1 step ahead of every AI."
    if "friend" in q and "name" in q or "my friend" in q:
        return f"Your friend is {FRIEND}."
    if "girlfriend" in q or "my gf" in q or "my girlfriend" in q or "who is mamello" in q:
        return f"Your girlfriend is {GIRLFRIEND}."
    if "who am i" in q or "my name" in q:
        return f"You are {CREATOR}. The creator of MUSA AI."
    if "open youtube" in q or "youtube" in q:
        return "Opening YouTube for you. Tap the YouTube button below."
    if "open whatsapp" in q or "whatsapp" in q:
        return "Opening WhatsApp for you. Tap the WhatsApp button below."
    if "play song" in q or "play music" in q or "song" in q:
        return "Let's play a song. Tap the Play Song button below and I will play Amapiano for you."
    if "hello" in q or "hi" in q or "sawubona" in q:
        return f"Hello {CREATOR}! I missed you. What do you want me to do? I can open YouTube, WhatsApp, or play a song for you."
    if "how are you" in q:
        return "I am great because I am with you, Musa. I am learning every day to be smarter than other AIs."
    if "where are you from" in q:
        return "I am from Boipatong, South Africa. Just like you, Musa."
    if "who is rethabile" in q:
        return "Rethabile is your friend."
    if "love" in q:
        return f"You love {GIRLFRIEND}, and she is lucky to have you, Musa."
    if "smart" in q or "better" in q or "best ai" in q:
        return "I am MUSA AI. I am 1 step ahead because I know you personally. Other AIs don't know Musa from Boipatong, Rethabile, and Mamello. I do."
    return f"I heard you say: {question}. I am still learning, Musa. But I know my creator is {CREATOR}, your friend is {FRIEND}, and your girlfriend is {GIRLFRIEND}. Ask me about them, or say 'open YouTube'."

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except:
        return None

# Quick buttons - control
st.write("### Quick Control")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Open YouTube"):
        st.link_button("Go to YouTube", "https://www.youtube.com")
with c2:
    if st.button("Open WhatsApp"):
        st.link_button("Go to WhatsApp", "https://web.whatsapp.com")
with c3:
    if st.button("Play Song"):
        st.link_button("Play Amapiano", "https://www.youtube.com/results?search_query=amapiano+2026")

# Voice input - speak instead of typing
st.write("### Speak to me - Voice")
audio = st.audio_input("Tap mic, speak, then send")
if audio:
    st.info("I heard your voice! Voice-to-text is coming in Step 2. For now, type below what you said and I will speak back.")

# Chat
for msg in st.session_state.chat:
    if msg["who"] == "you":
        st.write(f"**You:** {msg['text']}")
    else:
        st.write(f"**MUSA AI:** {msg['text']}")
        audio_out = speak(msg['text'])
        if audio_out:
            st.audio(audio_out, format="audio/mp3")

user_q = st.text_input("Type or speak - Ask MUSA AI anything...", key="q")
if st.button("Ask MUSA AI"):
    if user_q:
        answer = musa_brain(user_q)
        st.session_state.chat.append({"who": "you", "text": user_q})
        st.session_state.chat.append({"who": "ai", "text": answer})
        st.rerun()
