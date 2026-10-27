import streamlit as st
import google.generativeai as genai

# -----------------------------------------------------
# 1. Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="Intelligent Chat Assistant",
    page_icon="✨",
    layout="centered",
)

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
# 5. Session State
# -----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# -----------------------------------------------------
# 6. Helper Functions
# -----------------------------------------------------
def render_messages():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def get_ai_reply(user_message: str) -> str:
    try:
        response = st.session_state.chat.send_message(user_message)
        return response.text if getattr(response, "text", None) else "⚠️ AI could not generate a response."
    except Exception as e:
        return f"Sorry, I hit an error while generating a response: {e}"

# -----------------------------------------------------
# 7. UI Header
# -----------------------------------------------------
st.title("✨ Intelligent Chat Assistant")
st.caption("A friendly AI chatbot ready to chat with you 🤖💬")

# Sidebar actions
st.sidebar.title("Controls")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()

# -----------------------------------------------------
# 8. Render chat history
# -----------------------------------------------------
render_messages()

# -----------------------------------------------------
# 9. Chat input
# -----------------------------------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_reply = get_ai_reply(user_input)
        st.markdown(ai_reply)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
