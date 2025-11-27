import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# List models and pick first working
available = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]

if not available:
    st.error("No available Gemini text models found for your account.")
    st.stop()

model_name = available[0]  # or let user choose
model = genai.GenerativeModel(model_name)
