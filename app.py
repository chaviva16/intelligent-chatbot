import time
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
# 4. Model options with fallback support
# -----------------------------------------------------
MODEL_CANDIDATES = [
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
]

# -----------------------------------------------------
# 5. Session State
# -----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------
# 6. Helper Functions
# -----------------------------------------------------
def render_messages():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def recent_context(limit=6):
    recent = st.session_state.messages[-limit:]
    context = ""
    for msg in recent:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n\n"
    return context


def get_ai_reply(user_message: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\n{recent_context()}\nUser: {user_message}"

    last_error = None

    for model_name in MODEL_CANDIDATES:
        model = genai.GenerativeModel(model_name)

        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                return response.text if getattr(response, "text", None) else "⚠️ AI could not generate a response."
            except Exception as e:
                msg = str(e)
                last_error = msg

                # Retry transient timeouts or 504s
                if "504" in msg or "Deadline" in msg or "timed out" in msg.lower():
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue
                    break

                # If the model name is invalid or not available, try the next one.
                if "404" in msg or "not found" in msg.lower() or "not supported" in msg.lower():
                    break

                return f"Sorry, I hit an error while generating a response: {e}"

    if last_error:
        return f"The selected Gemini model is unavailable right now. Please try again in a moment. Details: {last_error}"

    return "The AI service is currently unavailable. Please try again."

# -----------------------------------------------------
# 7. UI Header
# -----------------------------------------------------
st.title("✨ Intelligent Chat Assistant")
st.caption("A friendly AI chatbot ready to chat with you 🤖💬")

# Sidebar actions
st.sidebar.title("Controls")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
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

    if len(st.session_state.messages) > 12:
        st.session_state.messages = st.session_state.messages[-12:]
