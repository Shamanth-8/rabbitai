import streamlit as st
import requests
import os

# Get backend URL from environment variable or use localhost as fallback
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')
API_URL = f"{BACKEND_URL}/analyze"
CODE_BUNNY_URL = f"{BACKEND_URL}/code-bunny"

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

            if response.status_code == 200:
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
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🐇 Code Bunny:** {msg['content']}")

# Add an empty placeholder at the end
scroll_anchor = st.empty()

# Force scroll into view using a tiny JS snippet
scroll_anchor.markdown(
    """
    <script>
    var chatDiv = window.parent.document.querySelector('.app');
    chatDiv.scrollTo(0, chatDiv.scrollHeight);
    </script>
    """,
    unsafe_allow_html=True
)

# Add this right after your imports
st.markdown("""
<style>
/* Base styles and dark theme */
.stApp {
    max-width: 100%;
    padding: 1rem;
    margin: 0 auto;
    background: linear-gradient(145deg, #1a1c1e 0%, #2d333b 100%);
}

/* Responsive Typography */
h1 {
    font-size: clamp(1.8rem, 4vw, 2.5rem) !important;
    color: #64ffda !important;
    margin-bottom: 2rem !important;
    text-align: center;
}

.stMarkdown {
    font-size: clamp(0.9rem, 2vw, 1rem);
}

/* Input Fields */
.stTextInput input, .stSelectbox select {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(100, 255, 218, 0.2) !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* File Uploader */
.stFileUploader {
    margin: 1rem 0;
}

.stFileUploader > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px dashed rgba(100, 255, 218, 0.3) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Buttons */
.stButton > button {
    width: 100% !important;
    padding: 0.6rem 1rem !important;
    background: linear-gradient(90deg, #64ffda 0%, #48bfe3 100%) !important;
    color: #1a1c1e !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: transform 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
}

/* Chat Messages */
.chat-message {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    word-wrap: break-word;
}

[data-testid="stMarkdown"] > div {
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
    margin: 0.5rem 0 !important;
}

/* User message */
[data-testid="stMarkdown"] > div:has(strong:contains("🧑 You:")) {
    background: rgba(100, 255, 218, 0.1) !important;
    border-left: 4px solid #64ffda !important;
}

/* Bot message */
[data-testid="stMarkdown"] > div:has(strong:contains("🐇 Code Bunny:")) {
    background: rgba(72, 191, 227, 0.1) !important;
    border-left: 4px solid #48bfe3 !important;
}

/* JSON Display */
.stJson {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    font-size: 0.9rem !important;
}

/* Responsive Layout */
@media screen and (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    
    .stButton > button {
        padding: 0.8rem !important;
    }
    
    [data-testid="stMarkdown"] > div {
        padding: 0.5rem !important;
    }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
    background: #64ffda;
    border-radius: 3px;
}

/* Loading Animation */
.stSpinner > div {
    border-color: #64ffda !important;
}

/* Error and Warning Messages */
.stAlert {
    border-radius: 8px !important;
    padding: 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)

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
