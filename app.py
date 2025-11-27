import streamlit as st
import google.generativeai as genai
import os

# ----------------------------------
# 1. PAGE CONFIG 
# ----------------------------------
st.set_page_config(page_title="Intelligent Chat Assistant", page_icon="✨")

# ----------------------------------
# 2. Load API Key (Streamlit Cloud uses st.secrets)
# ----------------------------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ----------------------------------
# 3. System Prompt
# ----------------------------------
system_prompt = """
You are an Intelligent Chat Assistant.

Guidelines:
- Give clear, accurate explanations.
- Use warm, friendly conversation.
- Break down complex topics simply.
- Give examples when needed.
- When writing code, add comments.
- If unsure, say “I’m not certain, but here’s my best suggestion.”
- Keep answers helpful and supportive.

Abilities:
- Data Science, ML, Python, SQL, AI
- Code writing and debugging
- Dates, fun facts, jokes, general conversation
"""

# ----------------------------------
# 4. Initialize Gemini Model 
# ----------------------------------
try:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

# ----------------------------------
# 5. Streamlit UI
# ----------------------------------
st.title("✨ Intelligent Chat Assistant")
st.write("A friendly AI chatbot ready to help you 🤖💬")


# ----------------------------------
# 6. Chat History
# ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ----------------------------------
# 7. Chat Function
# ----------------------------------
def get_response(prompt):
    chat_session = model.start_chat(history=st.session_state.messages)
    response = chat_session.send_message(prompt)
    return response.text


# ----------------------------------
# 8. Display previous chat history
# ----------------------------------
for message in st.session_state.messages:
    role = "🧑 You" if message["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {message['parts'][0]}")


# ----------------------------------
# 9. User Input
# ----------------------------------
user_input = st.text_input("Type your message here...")

if st.button("Send") or (user_input and user_input.strip() != ""):
    st.session_state.messages.append({"role": "user", "parts": [user_input]})
    ai_response = get_response(user_input)
    st.session_state.messages.append({"role": "model", "parts": [ai_response]})
    st.experimental_rerun()


# ----------------------------------
# 10. Clear chat
# ----------------------------------
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
