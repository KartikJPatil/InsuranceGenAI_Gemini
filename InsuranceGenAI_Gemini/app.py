# app.py
import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API Key (make sure it's set as env variable!)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="Insurance Support GenAI Agent (Gemini)")

st.title("🧑‍💼 Insurance Support GenAI Agent (Gemini)")
st.write("Ask your insurance-related questions and get instant answers powered by Gemini!")

user_input = st.text_area("Your question:", height=100, placeholder="e.g. What is the claim process for car insurance?")

if st.button("Get Answer"):
    if user_input.strip() != "":
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            answer = response.text
            st.success(answer)
    else:
        st.warning("Please enter a valid question.")
