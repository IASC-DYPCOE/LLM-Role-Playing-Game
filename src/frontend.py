import streamlit as st
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# Constants
API_ENDPOINT = "http://localhost:8000/dnd"


def set_fantasy_theme():
    """Set custom fantasy-themed CSS"""
    st.markdown(
        """
    <style>
        body { 
            color: #e0e0e0; 
            background-color: #1a1a2e; 
            font-family: 'Cinzel', serif; 
        }
        .stButton>button { 
            color: #ffd700; 
            background-color: #4a0e0e; 
            border: 2px solid #ffd700; 
        }
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea { 
            color: #e0e0e0; 
            background-color: #2a2a4e; 
        }
        .stHeader { 
            color: #ffd700; 
            text-shadow: 2px 2px 4px #000000; 
        }
        .sidebar .sidebar-content { 
            background-color: #16213e; 
        }
        .message-container {
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
            background-color: #2a2a4e;
            border: 1px solid #ffd700;
        }
        .dm-message {
            background-color: #4a0e0e;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap" rel="stylesheet">
    """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "Welcome, brave adventurer! I am your Dungeon Master. What would you like to do?",
            }
        ]
    if "game_active" not in st.session_state:
        st.session_state.game_active = False
    if "turn_count" not in st.session_state:
        st.session_state.turn_count = 0


def send_message_to_dm(message: str) -> Dict:
    """Send message to the DnD backend and get response"""
    try:
        response = requests.get(API_ENDPOINT, data={"form_input_text": message})
        return response.json()
    except Exception as e:
        st.error(f"Error communicating with Dungeon Master: {str(e)}")
        return {
            "content": "The Dungeon Master seems to be taking a break. Please try again."
        }


def main():
    st.set_page_config(page_title="🐉 TD-LLM-DND", page_icon="🐉", layout="wide")
    set_fantasy_theme()

    initialize_session_state()

    # Sidebar
    st.sidebar.title("🎲 Game Controls")

    if st.sidebar.button("🔄 Start New Game"):
        # st.session_state.messages = [
        #     {
        #         "role": "system",
        #         "content": "A new adventure begins! I am your Dungeon Master. What would you like to do?",
        #     }
        # ]
        send_message_to_dm("start new game")
        st.session_state.game_active = True
        st.session_state.turn_count = 0
        st.success("New game started!")

    if st.sidebar.button("⚔️ End Game"):
        st.session_state.game_active = False
        # st.session_state.messages.append(
        #     {
        #         "role": "system",
        #         "content": "The adventure has ended. Thank you for playing!",
        #     }
        # )

    st.title("🐉 TD-LLM-DND")

    if st.session_state.game_active:
        st.sidebar.metric("Turn Count", st.session_state.turn_count)

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            div_class = (
                "message-container dm-message"
                if msg["role"] == "system"
                else "message-container"
            )
            st.markdown(
                f"""
                <div class="{div_class}">
                    {msg["content"]}
                </div>
            """,
                unsafe_allow_html=True,
            )

    if st.session_state.game_active:
        with st.form(key="message_form", clear_on_submit=True):
            user_input = st.text_area(
                "What do you do?",
                key="input",
                placeholder="Describe your action...",
                height=100,
            )
            submit_button = st.form_submit_button("🎲 Take Action")

            if submit_button and user_input:
                st.session_state.messages.append(
                    {"role": "user", "content": user_input}
                )
                st.session_state.turn_count += 1

                with st.spinner("The Dungeon Master ponders your action..."):
                    dm_response = send_message_to_dm(user_input)

                    st.session_state.messages.append(
                        {
                            "role": "system",
                            "content": dm_response.get(
                                "content",
                                "The Dungeon Master is momentarily lost in thought...",
                            ),
                        }
                    )

                st.experimental_rerun()
    else:
        st.info("👆 Click 'Start New Game' in the sidebar to begin your adventure!")

    st.sidebar.markdown("""
    ## How to Play
    1. Start a new game
    2. Describe your actions
    3. React to the DM's responses
    4. End game when finished
    
    May your dice rolls be ever in your favor! 🎲
    """)


if __name__ == "__main__":
    main()
