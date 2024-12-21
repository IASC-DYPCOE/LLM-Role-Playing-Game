import streamlit as st
import requests
from typing import Dict


def initialize_session_state():
    """Initialize session state for chat messages."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "Welcome, brave adventurer! I am your Dungeon Master. What would you like to do?",
            }
        ]


def send_message(message: str) -> Dict:
    """Send message to the DnD backend and get response."""
    try:
        url = "http://127.0.0.1:8000/dnd/play"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"input_text": message}

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with DM: {e}")
        return {"content": "Sorry, I encountered an error. Please try again."}


def start_game():
    """Start a new game and initialize the chat history."""
    try:
        response = requests.get("http://localhost:8000/dnd/start")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error starting the game: {e}")
        return {"content": "Sorry, I encountered an error. Please try again."}


st.set_page_config(page_title="DnD RPG Chat", page_icon="🎲", layout="wide")

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
    }
    .dm-message {
        background-color: #383838;
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

initialize_session_state()

st.title("🎲 DnD Adventure")

if st.button("Start New Game"):
    with st.spinner("Starting a new adventure..."):
        game_response = start_game()
        # if "content" in game_response:
        #     st.session_state.messages = [
        #         {"role": "system", "content": game_response["content"]}
        #     ]
        #     st.success("The game has started! Let your adventure begin.")
        # else:
        #     st.error("Failed to start the game. Please try again.")
        st.write(game_response)

with st.container():
    for msg in st.session_state.messages:
        div_class = "user-message" if msg["role"] == "user" else "dm-message"
        st.markdown(
            f"""
            <div class="message-container {div_class}">
                {msg["content"]}
            </div>
            """,
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
