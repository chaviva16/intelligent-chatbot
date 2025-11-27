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
# 3. System Prompt (hidden)
# -----------------------------
system_prompt = """
You are an Intelligent Chat Assistant.

Rules:
- Always give concise, accurate answers.
- Do not add extra facts unless asked.
- Keep responses simple, clear, and relevant.
- Use warm, friendly language.
- When writing code, provide clean Python code with comments.
"""

# -----------------------------
# 4. Initialize Gemini Model
# -----------------------------
model = genai.GenerativeModel("gemini-flash-latest")

# -----------------------------
# 5. Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 6. Streamlit UI
# -----------------------------
st.title("✨ Intelligent Chat Assistant")
st.write("A friendly AI chatbot ready to chat with you 🤖💬")

# -----------------------------
# 7. Chat Function with real-time date and safety handling
# -----------------------------
def get_response(prompt):
    # Add current date and time
    current_datetime = datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
    prompt_with_context = f"Current date and time: {current_datetime}\nUser asked: {prompt}"

    # Hidden system prompt in history
    chat_history = [{"role": "user", "parts": [system_prompt]}] + st.session_state.messages
    chat = model.start_chat(history=chat_history)

    response = chat.send_message(prompt_with_context)

    # Safety check and fallback
    if hasattr(response, "text") and response.text:
        return response.text
    elif hasattr(response, "candidates") and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, "content"):
            return candidate.content
    return "⚠️ Sorry, I couldn't generate a response. It may have been blocked for safety reasons."

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
# 9. User Input using form (auto-reset)
# -----------------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    submit_button = st.form_submit_button("Send")
    if submit_button and user_input.strip() != "":
        # Save user message
        st.session_state.messages.append({"role": "user", "parts": [user_input]})
        # Get AI response
        ai_response = get_response(user_input)
        st.session_state.messages.append({"role": "model", "parts": [ai_response]})

# -----------------------------
# 10. Clear Chat Button
# -----------------------------
if st.button("Clear Chat"):
    st.session_state.messages = []
