import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.title("Code Pilot")

problem = st.text_input("Enter the problem and your approach")
uploaded_file = st.file_uploader("Upload your Python code", type=["py", "txt"])
level = st.selectbox(
    "Choose your level",
    [
        "Baby Leetcoder",
        "Knight of Arrays",
        "Algorithm Wizard",
        "Leetcode Dragon Slayer"
    ]
)
level_map = {
    "Baby Leetcoder": "beginner",
    "Knight of Arrays": "intermediate",
    "Algorithm Wizard": "better than most",
    "Leetcode Dragon Slayer": "the best out there"
}
user_level=level_map[level]
if st.button("Submit"):
    if not problem:
        st.warning("Please enter the problem and your approach.")
    elif not level:
        st.warning("Please choose your level.")
    elif not uploaded_file:
        st.warning("Please upload your code.")
    else:
        try:
            files = {"file": uploaded_file.getvalue()}
            data = {"problem": problem, "level": user_level}

            response = requests.post(API_URL, files={"file": uploaded_file}, data=data)

            if response.status_code == 200:
                result = response.json()

                st.subheader("Static Analysis")
                st.json(result["analysis"])

                st.subheader("AI Insights")
                st.write(result["ai_insights"])
            else:
                st.error(f"Error connecting to backend: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")
    
