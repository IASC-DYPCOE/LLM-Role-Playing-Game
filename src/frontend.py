import streamlit as st
from audio import AudioUtils
from utils import extract_lives_remaining
from llm import DungeonMaster

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "dm" not in st.session_state:
    st.session_state.dm = DungeonMaster()
    st.session_state.au = AudioUtils()

st.set_page_config(page_title="DnD RPG Chat", page_icon="🧙🏽", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .message-container {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #FFFFFF;
    }
    .user-message {
        background-color: #2D2D2D;
        text-align: right;
        margin-left: 20%;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .dm-message {
        background-color: #383838;
        margin-right: 20%;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .chat-container {
        margin-bottom: 20px;
        padding: 10px;
    }
    input[type="text"] {
        background-color: #2D2D2D !important;
        color: white !important;
        border-color: #4D4D4D !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧙🏽 DnD Adventure")


def start_new_game():
    st.session_state.chat_history = []
    st.session_state.dm = DungeonMaster()
    response = st.session_state.dm.inference(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "dm", "content": response})
    return response


def send_message(message: str) -> str:
    response = st.session_state.dm.inference(st.session_state.chat_history, message)
    st.session_state.chat_history.append({"role": "user", "content": message})
    st.session_state.chat_history.append({"role": "dm", "content": response})
    return response


if st.button("Start New Game"):
    with st.spinner("Starting a new adventure..."):
        game_response = start_new_game()

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f'<div class="user-message">{message["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="dm-message">{message["content"]}</div>',
            unsafe_allow_html=True,
        )

with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your action:", key="input", placeholder="What would you like to do?"
    )
    submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        with st.spinner("The Dungeon Master is thinking..."):
            dm_response = send_message(user_input)
            st.write(dm_response)
            st.metric(
                label="Lives Remaining",
                value=extract_lives_remaining(dm_response),
                border=True,
            )
