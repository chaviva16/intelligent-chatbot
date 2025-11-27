import streamlit as st
import google.generativeai as genai
from datetime import datetime

# -----------------------------
# 1. Page Config
# -----------------------------
st.set_page_config(page_title="Intelligent Chat Assistant", page_icon="✨")

# -----------------------------
# 2. Load API Key
# -----------------------------
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# -----------------------------
# 3. System Prompt 
# -----------------------------
system_prompt = """
You are an Intelligent Chat Assistant.

Rules:
- Always give concise, accurate answers.
- Do not add extra facts unless asked.
- Keep responses simple, clear, and relevant.
- Use warm, friendly language.
- When writing code, provide clean Python code with comments.

Abilities:
- Answer questions about Data Science, ML, Python, SQL, AI.
- Write and debug code.
- Provide general conversation, date, time, and direct answers.
"""

# -----------------------------
# 4. Initialize Gemini Model
# -----------------------------
model = genai.GenerativeModel("gemini-flash-latest")

# -----------------------------
# 5. Chat History
# -----------------------------
if "messages" not in st.session_state:
    # only store real messages, system_prompt is kept separately for the model
    st.session_state.messages = []

# -----------------------------
# 6. Streamlit UI
# -----------------------------
st.title("✨ Intelligent Chat Assistant")
st.write("A friendly AI chatbot ready to chat with you 🤖💬")

# -----------------------------
# 7. Chat Function
# -----------------------------
def get_response(prompt):
    # Prepare history for model (include system_prompt but not displayed)
    chat_history = [{"role": "user", "parts": [system_prompt]}] + st.session_state.messages
    chat = model.start_chat(history=chat_history)
    response = chat.send_message(prompt)
    return response.text

# -----------------------------
# 8. Display Chat History
# -----------------------------
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div style="text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px;">
        🧑 You: {message['parts'][0]}
        </div>
        """, unsafe_allow_html=True)
    elif message["role"] == "model":
        st.markdown(f"""
        <div style="text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px;">
        🤖 AI: {message['parts'][0]}
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 9. User Input
# -----------------------------
# Use session_state to auto-clear input
if "input_value" not in st.session_state:
    st.session_state.input_value = ""

user_input = st.text_input("Type your message here...", key="input_value")

if st.button("Send") and user_input.strip() != "":
    # Save user message
    st.session_state.messages.append({"role": "user", "parts": [user_input]})
    # Get AI response
    ai_response = get_response(user_input)
    st.session_state.messages.append({"role": "model", "parts": [ai_response]})
    # Clear input for next question
    st.session_state.input_value = ""
