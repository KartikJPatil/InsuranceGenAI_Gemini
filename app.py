# app.py
import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# ✅ 1. Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ 2. Load CSV data for Claims and Product Recommendation
claims_df = pd.read_csv("claims.csv")
products_df = pd.read_csv("products.csv")

# ✅ 3. Streamlit UI Setup
st.set_page_config(page_title="Insurance Support GenAI Agent (Gemini)")

st.title("🧑‍💼 Insurance Support GenAI Agent (Gemini 1.5 Flash)")

# ✅ 4. Select Language
language = st.selectbox(
    "Select your preferred language:",
    ["English", "Hindi", "Marathi"]
)

# ✅ 5. Choose Feature
option = st.radio(
    "What would you like to do?",
    ["General Insurance Q&A", "Check Claim Status", "Product Recommendation"]
)

# ✅ 6. Claims Status Checker
if option == "Check Claim Status":
    claim_id = st.text_input("Enter your Claim ID (e.g., CLM12345):")
    if st.button("Check Status"):
        if claim_id in claims_df['ClaimID'].values:
            status = claims_df.loc[claims_df['ClaimID'] == claim_id, 'Status'].values[0]
            st.success(f"✅ Your claim status is: **{status}**")
        else:
            st.warning("Claim ID not found. Please check your ID.")

# ✅ 7. Product Recommendation Engine
elif option == "Product Recommendation":
    age = st.number_input("Your age:", min_value=18, max_value=100, step=1)
    coverage = st.selectbox(
        "Type of coverage you want:",
        ["Health", "Life", "Vehicle"]
    )
    if st.button("Recommend a Policy"):
        recommended = products_df[
            (products_df['Coverage'].str.lower() == coverage.lower()) &
            (products_df['TargetAge'].str.contains(f"{age//10*10}-{age//10*10+10}"))
        ]
        if not recommended.empty:
            row = recommended.iloc[0]
            st.success(f"✅ Recommended Policy:\n\n"
                       f"- Name: {row['PolicyName']}\n"
                       f"- Coverage: {row['Coverage']}\n"
                       f"- Premium: ₹{row['Premium']}")
        else:
            st.warning("Sorry, no matching policy found for your inputs.")

# ✅ 8. General Insurance Q&A with Language Support
else:
    user_input = st.text_area("Ask your insurance-related question:", height=100)
    if st.button("Get Answer"):
        if user_input.strip():
            lang_instruction = ""
            if language == "Hindi":
                lang_instruction = " Respond in Hindi."
            elif language == "Marathi":
                lang_instruction = " Respond in Marathi."

            prompt = (
                "You are an expert insurance assistant. "
                "Answer ONLY insurance-related queries about policies, claims, or product recommendations. "
                "If the question is unrelated to insurance, respond: "
                "'Sorry, I can only help with insurance-related queries.' "
                + lang_instruction +
                f"\n\nUser: {user_input}"
            )

            response = model.generate_content(prompt)
            answer = response.text
            st.success(answer)
        else:
            st.warning("Please enter a valid question.")
