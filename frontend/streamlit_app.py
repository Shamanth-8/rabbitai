import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.title("Code pilot")

uploaded_file = st.file_uploader("Upload your Python code", type=["py", "txt"])

if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(API_URL, files={"file": uploaded_file})
    
    if response.status_code == 200:
        result = response.json()
        
        st.subheader("Static Analysis")
        st.json(result["analysis"])
        
        st.subheader("AI Insights")
        st.write(result["ai_insights"])
    else:
        st.error("Error connecting to backend")
