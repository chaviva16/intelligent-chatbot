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
# 4. Discover an available Gemini model dynamically
# -----------------------------------------------------
def get_available_model_name():
    try:
        models = genai.list_models()
    except Exception as e:
        return None, f"Unable to list models: {e}"

    candidates = []
    for model in models:
        methods = getattr(model, "supported_generation_methods", []) or []
        if "generateContent" in methods:
            name = getattr(model, "name", "")
            if name:
                candidates.append(name)

    if not candidates:
        return None, "No Gemini models with generateContent support were returned by the API."

    # Prefer recent, widely-supported Gemini models.
    preferred_order = [
        "models/gemini-2.0-flash",
        "models/gemini-2.5-flash",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-flash-latest",
    ]

    for preferred in preferred_order:
        if preferred in candidates:
            return preferred.split("/")[-1], None

    # Fallback to the first available model if no preferred one is returned.
    return candidates[0].split("/")[-1], None


MODEL_NAME, MODEL_ERROR = get_available_model_name()
MODEL = None if MODEL_NAME is None else genai.GenerativeModel(MODEL_NAME)

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
    if MODEL is None:
        return (
            "The Gemini API is not available for this account or API key. "
            f"Please check your API configuration. Details: {MODEL_ERROR}"
        )

    prompt = f"{SYSTEM_PROMPT}\n\n{recent_context()}\nUser: {user_message}"

    for attempt in range(3):
        try:
            response = MODEL.generate_content(prompt)
            return response.text if getattr(response, "text", None) else "⚠️ AI could not generate a response."
        except Exception as e:
            msg = str(e)
            if "504" in msg or "Deadline" in msg or "timed out" in msg.lower():
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                return "The AI service is temporarily slow. Please try again in a moment."

            if "404" in msg or "not found" in msg.lower() or "not supported" in msg.lower():
                return (
                    "The current Gemini model is not available for this API key or project. "
                    "Please check your Google AI Studio / Google Cloud configuration and redeploy after updating the key."
                )

            return f"Sorry, I hit an error while generating a response: {e}"

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
