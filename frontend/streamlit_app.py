import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"
CODE_BUNNY_URL = "http://127.0.0.1:8000/code-bunny"

# --- Custom CSS ---
st.markdown("""
<style>
/* General Styles */
body {
    color: #E0E0E0;
}
.stApp {
    background-color: #1E1E1E;
    border-radius: 15px;
    padding: 2rem;
    font-family: 'Courier New', Courier, monospace;
}
h1 {
    color: #FFA726; /* A nice orange */
    text-align: center;
    font-family: 'monospace';
    letter-spacing: 3px;
}
h2, h3 {
    color: #81D4FA; /* Light blue */
}
/* --- Button Styles --- */
.stButton>button {
    border: 2px solid #FFA726;
    background-color: transparent;
    color: #FFA726;
    padding: 10px 24px;
    border-radius: 50px;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background-color: #FFA726;
    color: #1E1E1E;
    border-color: #FFA726;
}
.stButton>button:active {
    transform: scale(0.95);
}
/* --- Input & Uploader Styles --- */
.stTextInput>div>div>input, .stFileUploader>div, .stSelectbox>div {
    border: 2px solid #81D4FA;
    background-color: #333333;
    color: #E0E0E0;
    border-radius: 10px;
}
.stFileUploader>div>button {
    border: none;
    background-color: #81D4FA;
    color: #1E1E1E;
}
/* --- Chat Styles --- */
[data-testid="stChatMessage"] {
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
[data-message-author-role="user"] > div > div {
    background-color: #4CAF50; /* A shade of green */
}
[data-message-author-role="assistant"] > div > div {
    background-color: #03A9F4; /* A shade of blue */
}
</style>
""", unsafe_allow_html=True)

st.title("Code Bunny")

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

user_level = level_map[level]

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # will store dicts like {"role": "user"/"assistant", "content": "..."}

# --- Step 1: Run Analysis ---
if st.button("Submit for Analysis"):
    if not problem:
        st.warning("Please enter the problem and your approach.")
    elif not level:
        st.warning("Please choose your level.")
    elif not uploaded_file:
        st.warning("Please upload your code.")
    else:
        try:
            data = {"problem": problem, "level": user_level}
            response = requests.post(
                API_URL,
                files={"file": uploaded_file},
                data=data)

            if response.status_code == 2.00:
                result = response.json()
                st.session_state.analysis_result = result
                st.session_state.chat_history = []  # reset chat when new analysis runs

                st.subheader("Static Analysis")
                st.json(result["analysis"])

                st.subheader("AI Insights")
                st.write(result["ai_insights"])
            else:
                st.error(f"Error connecting to backend: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")


# --- Step 2: Chat with Code Bunny ---
st.subheader("Talk to Code Bunny")
user_prompt = st.text_input("Your message to Code Bunny")

if st.button("Send to Code Bunny"):
    if not st.session_state.analysis_result:
        st.warning("Run analysis first before chatting with Code Bunny.")
    elif not user_prompt.strip():
        st.warning("Type something for Code Bunny!")
    else:
        try:
            response = requests.post(
                CODE_BUNNY_URL,
                json={
                    "analysis_result": st.session_state.analysis_result,
                    "chat_history": st.session_state.chat_history,
                    "user_prompt": user_prompt
                }
            )

            if response.status_code == 200:
                bunny_reply = response.json().get("reply", "No reply 🤔")

                # Save both user & bot messages
                st.session_state.chat_history.append({"role": "user", "content": user_prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": bunny_reply})
            else:
                st.error(f"Error from Code Bunny: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# --- Show chat history ---
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🐇"):
            st.markdown(msg["content"])


if __name__ == "__main__":
    import subprocess
    import sys
    print("🎨 Starting Code Bunny Frontend...")
    print("🌐 Frontend will be available at: http://127.0.0.1:8501")
    print("Press Ctrl+C to stop the app")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        __file__,
        "--server.port", "8501"
    ])
