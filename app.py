import streamlit as st
import google.generativeai as genai
import os

# ----------------------------------
# 1. Streamlit Page Config
# ----------------------------------
st.set_page_config(page_title="Intelligent Chat Assistant", page_icon="✨")

# ----------------------------------
# 2. Load Gemini API Key
# ----------------------------------

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
else:
    genai.configure(api_key=api_key)

# ----------------------------------
# 3. System Prompt
# ----------------------------------
system_prompt = """
You are an Intelligent Chat Assistant.

Guidelines:
- Give clear, accurate explanations.
- Speak in warm, friendly, conversational language.
- Break down complex topics simply.
- Provide examples when needed.
- When asked for code, write clean Python code with comments.
- Break down code line-by-line when explaining.
- When unsure, say “I’m not certain, but here’s my best suggestion.”
- Keep answers helpful, calm, and supportive.

Abilities:
- Explain Data Science, ML, Python, SQL, AI.
- Write and debug code.
- Tell jokes, dates, fun facts, general conversation.
"""

# ----------------------------------
# 4. Initialize Gemini Model (FIXED)
# ----------------------------------
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=system_prompt
)

# ----------------------------------
# 5. Streamlit UI
# ----------------------------------
st.title("✨ Intelligent Chat Assistant")
st.write("A friendly AI assistant ready to chat with you!")

# ----------------------------------
# 6. Chat History
# ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# 7. Chat Function
# ----------------------------------
def get_response(prompt):
    chat = model.start_chat(history=st.session_state.messages)
    response = chat.send_message(prompt)
    return response.text

# ----------------------------------
# 8. Display Chat History
# ----------------------------------
for message in st.session_state.messages:
    role = "🧑‍💻 You" if message["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {message['parts'][0]}")

# ----------------------------------
# 9. User Input
# ----------------------------------
user_input = st.text_input("Type your message here...")

if st.button("Send") or (user_input and user_input.strip() != ""):
    # Save user message
    st.session_state.messages.append({"role": "user", "parts": [user_input]})

    # Get AI response
    ai_response = get_response(user_input)

    # Save AI response
    st.session_state.messages.append({"role": "model", "parts": [ai_response]})

    st.experimental_rerun()

# ----------------------------------
# 10. Clear Chat Button
# ----------------------------------
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
