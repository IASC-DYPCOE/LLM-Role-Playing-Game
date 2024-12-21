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
        response = requests.post(  # Use POST for sending data
            "http://localhost:8000/dnd",
            json={"form_input_text": message},  # Correct payload format
        )
        response.raise_for_status()  # Raise exception for HTTP errors
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


# Set up the Streamlit app configuration
st.set_page_config(page_title="DnD RPG Chat", page_icon="🎲", layout="wide")

# Add custom CSS for styling
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

# Initialize session state
initialize_session_state()

# App title
st.title("🎲 DnD Adventure")

# Chat container
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

# Input form for user action
with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your action:", key="input", placeholder="What would you like to do?"
    )
    submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        # Append user's message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get Dungeon Master's response
        with st.spinner("The Dungeon Master is thinking..."):
            dm_response = send_message(user_input)

            # Append DM's response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": dm_response.get(
                        "content", "Something went wrong. Please try again."
                    ),
                }
            )
