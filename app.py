import streamlit as st
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="Intelligent Chat Assistant", page_icon="✨")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-flash-latest")

SYSTEM_PROMPT = """
You are an Intelligent Chat Assistant.
Give concise, warm, and accurate answers.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

def format_chat_history():
    txt = ""
    for m in st.session_state.messages:
        role = "User" if m["role"] == "user" else "AI"
        txt += f"{role}: {m['parts'][0]}\n"
    return txt

def respond(prompt):
    now = datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
    final_prompt = f"""
{SYSTEM_PROMPT}

Current date/time: {now}

Chat history:
{format_chat_history()}

User: {prompt}
AI:
"""
    resp = model.generate_content(final_prompt)
    return resp.text or "⚠️ Couldn't generate a response."

st.title("✨ Intelligent Chat Assistant")

# Show chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="text-align:right;background:#DCF8C6;padding:10px;border-radius:8px;margin:5px">
            🧑 <b>You:</b> {msg['parts'][0]}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="text-align:left;background:#F1F0F0;padding:10px;border-radius:8px;margin:5px">
            🤖 <b>AI:</b> {msg['parts'][0]}
            </div>
            """,
            unsafe_allow_html=True,
        )

# 🚀 INSTANT INPUT — no form, no double-click
user_msg = st.text_input("Type your message and press Enter:", key="chat_input")

if user_msg:
    st.session_state.messages.append({"role": "user", "parts": [user_msg]})
    reply = respond(user_msg)
    st.session_state.messages.append({"role": "model", "parts": [reply]})
    st.session_state.chat_input = ""  # reset input
    st.experimental_rerun()

# Clear chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
