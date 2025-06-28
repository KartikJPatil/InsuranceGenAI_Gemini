# app.py
import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API Key (from Streamlit secrets or env)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model (using Gemini 1.5 Flash or Pro)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="Insurance Support GenAI Agent (Gemini)")

st.title("🧑‍💼 Insurance Support GenAI Agent (Gemini 1.5 Flash)")
st.write("Ask your insurance-related questions and get instant answers powered by Gemini 1.5 Flash!")

user_input = st.text_area("Your question:", height=100, placeholder="e.g. What is the claim process for car insurance?")

if st.button("Get Answer"):
    if user_input.strip() != "":
        with st.spinner("Thinking..."):
            # Use a focused prompt to restrict answers
            prompt = (
                "You are an expert insurance customer support agent. "
                "Answer ONLY questions related to insurance policies, claims, or product recommendations. "
                "If the question is unrelated to insurance, politely respond with: "
                "'Sorry, I can only help with insurance-related queries.'\n\n"
                f"User: {user_input}"
            )
            response = model.generate_content(prompt)
            answer = response.text
            st.success(answer)
    else:
        st.warning("Please enter a valid question.")
