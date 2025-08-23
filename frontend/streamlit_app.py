import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"
CODE_BUNNY_URL = "http://127.0.0.1:8000/code-bunny"

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
