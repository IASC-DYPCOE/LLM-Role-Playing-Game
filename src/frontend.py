import streamlit as st
import time
import random
from utils import extract_lives_remaining
from llm import DungeonMaster

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "dm" not in st.session_state:
    st.session_state.dm = DungeonMaster()

st.set_page_config(page_title="DnD RPG Chat", page_icon="🧙🏽", layout="wide")

# Enhanced CSS
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1599058917212-d6f5e99e4946") no-repeat center center fixed;
        background-size: cover;
        color: #E0C097;
        font-family: 'Cinzel', serif;
    }
    .message-container {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: rgba(77, 45, 45, 0.8);
        text-align: right;
        margin-left: 20%;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
    }
    .dm-message {
        background-color: rgba(40, 40, 40, 0.9);
        margin-right: 20%;
        padding: 10px;
        border-radius: 10px;
        font-style: italic;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
    }
    .typing-animation {
        font-style: italic;
        color: #FFD700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("🧙🏽 DnD Adventure")


# Start a new game
def start_new_game():
    st.session_state.chat_history = []
    st.session_state.dm = DungeonMaster()
    response = st.session_state.dm.inference(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "dm", "content": response})
    return response


# Handle sending message
def send_message(message: str) -> str:
    response = st.session_state.dm.inference(st.session_state.chat_history, message)
    st.session_state.chat_history.append({"role": "user", "content": message})
    st.session_state.chat_history.append({"role": "dm", "content": response})
    return response


# Start Game Button
if st.button("⚔️ Start New Game"):
    with st.spinner("Summoning the Dungeon Master..."):
        game_response = start_new_game()

# Display Chat History
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">🧝‍♂️ {message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="dm-message">🧙‍♂️ {message["content"]}</div>',
                unsafe_allow_html=True,
            )

# User Input Form
with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your action:", key="input", placeholder="What would you like to do?"
    )
    submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        with st.spinner("The Dungeon Master is thinking..."):
            with st.empty():  # Typing Animation
                for _ in range(3):
                    st.markdown(
                        '<p class="typing-animation">🧙‍♂️ The DM is thinking...</p>',
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.5)
                    st.markdown("")  # Clear animation
            dm_response = send_message(user_input)
            st.write(dm_response)
            st.metric(
                label="Turns Remaining", value=extract_lives_remaining(dm_response)
            )
