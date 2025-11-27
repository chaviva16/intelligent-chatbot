import streamlit as st
import google.generativeai as genai

# -----------------------------
# 1. Page Config
# -----------------------------
st.set_page_config(page_title="Intelligent Chat Assistant", page_icon="✨")

# -----------------------------
# 2. Load API Key
# -----------------------------
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API key not found. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# -----------------------------
# 3. System Prompt
# -----------------------------
system_prompt = """
You are an Intelligent Chat Assistant.

Guidelines:
- Clear, accurate explanations
- Warm, friendly conversation
- Break down complex topics
- Provide examples
- Write clean code with comments
- If unsure, say “I’m not certain, but here’s my best suggestion.”
- Keep answers helpful and supportive

Abilities:
- Data Science, ML, Python, SQL, AI
- Code writing and debugging
- Dates, fun facts, jokes, general conversation
"""

# -----------------------------
# 4. Initialize Gemini Model
# -----------------------------
model = genai.GenerativeModel("gemini-flash-latest")

# -----------------------------
# 5. Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "parts": [system_prompt]}]

# -----------------------------
# 6. Streamlit UI
# -----------------------------
st.title("✨ Intelligent Chat Assistant")
st.write("A friendly AI chatbot ready to chat with you 🤖💬")

# -----------------------------
# 7. Chat Function
# -----------------------------
def get_response(prompt):
    chat_session = model.start_chat(history=st.session_state.messages)
    response = chat_session.send_message(prompt)
    return response.text

# -----------------------------
# 8. Display Chat History with bubbles
# -----------------------------
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    if message["role"] == "user":
        st.markdown(f"""
        <div style="text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px;">
        🧑 You: {message['parts'][0]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px;">
        🤖 AI: {message['parts'][0]}
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 9. User Input
# -----------------------------
user_input = st.text_input("Type your message here...", key="input")

if st.button("Send"):
    if user_input.strip() != "":
        st.session_state.messages.append({"role": "user", "parts": [user_input]})
        ai_response = get_response(user_input)
        st.session_state.messages.append({"role": "model", "parts": [ai_response]})
        st.session_state.input = ""  # Clear input box

# -----------------------------
# 10. Clear Chat Button
# -----------------------------
if st.button("Clear Chat"):
    st.session_state.messages = [{"role": "system", "parts": [system_prompt]}]
    st.session_state.input = ""
