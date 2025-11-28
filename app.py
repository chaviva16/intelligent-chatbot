import streamlit as st
import google.generativeai as genai
from datetime import datetime

# -----------------------------------------------------
# 1. Page Config
# -----------------------------------------------------
st.set_page_config(page_title="Intelligent Chat Assistant", page_icon="✨")

# -----------------------------------------------------
# 2. Load API Key
# -----------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# -----------------------------------------------------
# 3. System Prompt
# -----------------------------------------------------
SYSTEM_PROMPT = """
You are an Intelligent Chat Assistant.

Rules:
- Give concise, accurate answers.
- Keep language warm, friendly, and simple.
- Do not add unnecessary information.
- Provide clean Python code when required.
"""

# -----------------------------------------------------
# 4. Initialize model
# -----------------------------------------------------
model = genai.GenerativeModel("gemini-flash-latest")

# -----------------------------------------------------
# 5. Session State for Messages
# -----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------
# 6. Format Chat History
# -----------------------------------------------------
def format_chat_history():
    history_text = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "AI"
        history_text += f"{role}: {msg['parts'][0]}\n"
    return history_text

# -----------------------------------------------------
# 7. Fast Response Function
# -----------------------------------------------------
def get_fast_response(user_message):
    current_datetime = datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")

    full_prompt = f"""
{SYSTEM_PROMPT}

Current date and time: {current_datetime}

Chat history:
{format_chat_history()}

User: {user_message}
AI:
"""

    response = model.generate_content(full_prompt)
    return getattr(response, "text", "⚠️ AI could not generate a response.")

# -----------------------------------------------------
# 8. Custom CSS for Beautiful Chat Bubbles
# -----------------------------------------------------
st.markdown("""
<style>

.chat-user {
    background-color: #C8F7C5;
    color: #000;
    padding: 10px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

.chat-ai {
    background-color: #ECECEC;
    color: #000;
    padding: 10px;
    border-radius: 12px;
    margin: 8px 0;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# 9. UI Header
# -----------------------------------------------------
st.title("✨ Intelligent Chat Assistant")
st.write("A friendly AI chatbot ready to chat with you 🤖💬")

# -----------------------------------------------------
# 10. Show Chat Messages
# -----------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-user'>🧑 <b>You:</b> {msg['parts'][0]}</div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div class='chat-ai'>🤖 <b>AI:</b> {msg['parts'][0]}</div>",
            unsafe_allow_html=True)

# -----------------------------------------------------
# 11. Input Form 
# -----------------------------------------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append({"role": "user", "parts": [user_input]})
        ai_reply = get_fast_response(user_input)
        st.session_state.messages.append({"role": "model", "parts": [ai_reply]})

# -----------------------------------------------------
# 12. Clear Chat Button
# -----------------------------------------------------
if st.button("Clear Chat"):
    st.session_state.messages = []
