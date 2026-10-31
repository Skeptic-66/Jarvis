import json
import streamlit as st
import streamlit.components.v1 as components
from google import genai

st.title("Jarvis")
voice = st.sidebar.toggle("Voice", value=True)

if "chat" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-flash-lite-latest",
        config={"system_instruction": "You are Jarvis, a smart, helpful, honest assistant. Answer clearly and directly."},
    )
    st.session_state.msgs = []

def speak(text):
    components.html(
        f"""<script>
        const u = new SpeechSynthesisUtterance({json.dumps(text)});
        u.pitch = 0.5; u.rate = 0.95;
        speechSynthesis.cancel();
        speechSynthesis.speak(u);
        </script>""",
        height=0,
    )

for m in st.session_state.msgs:
    st.chat_message(m["role"]).write(m["text"])

if p := st.chat_input("Ask Jarvis"):
    st.chat_message("user").write(p)
    reply = st.session_state.chat.send_message(p).text
    st.chat_message("assistant").write(reply)
    st.session_state.msgs += [{"role": "user", "text": p}, {"role": "assistant", "text": reply}]
    if voice:
        speak(reply)