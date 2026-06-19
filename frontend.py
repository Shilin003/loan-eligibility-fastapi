import streamlit as st
import requests

st.set_page_config(page_title="Loan Approver", page_icon="🏦")

st.title("🏦 Bank Loan Eligibility Approver")
st.write("Fill out the application below to see if our AI will approve your loan.")

# Create input boxes for the user
age = st.number_input("Age", min_value=0, max_value=120, value=30)
income = st.number_input("Annual Income ($)", min_value=0, value=50000, step=5000)
credit_score = st.number_input("Credit Score", min_value=0, max_value=900, value=700)

# When the user clicks the submit button...
if st.button("Submit Application", type="primary"):
    
    # 1. Package the data into a JSON dictionary
    payload = {
        "age": age,
        "income": income,
        "credit_score": credit_score
    }
    
    # 2. Send the note to your FastAPI Docker container
    api_url = "http://127.0.0.1:8000/predict"
    
    try:
        response = requests.post(api_url, json=payload)
        
        # 3. Read the answer and show the result to the user
        if response.status_code == 200:
            result = response.json()
            if result["loan_approved"]:
                st.success(f"🎉 Congratulations! You are APPROVED. (Confidence: {result['approval_probability']:.2f})")
            else:
                st.error(f"❌ Sorry, your application was DENIED. (Confidence: {result['approval_probability']:.2f})")
                
        # If Pydantic catches a bad number (like age 0)
        elif response.status_code == 422:
            st.warning("⚠️ Our system rejected the data! Please ensure your numbers are valid (e.g., Age must be 18+).")
            
    except requests.exceptions.ConnectionError:
        st.error("🔌 Could not connect to the AI. Is your Docker container running on port 8000?")