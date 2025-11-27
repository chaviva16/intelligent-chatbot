import google.generativeai as genai
import streamlit as st

api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.title("Available Gemini Models")

# List models that support content generation
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        st.write(m.name)
