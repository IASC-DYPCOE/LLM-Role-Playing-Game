import matplotlib.pyplot as plt
import streamlit as st
from typing import Dict
from llm import DuengeonMaster

duengeon_master = DuengeonMaster()


def send_message(message: str) -> Dict:
    """Send message to the DnD backend and get response."""
    response = duengeon_master.inference(message)
    return response


def start_game():
    """Start a new game and initialize the chat history."""
    response = duengeon_master.inference()
    return response


def draw_lives_chart(remaining_lives):
    if remaining_lives < 0 or remaining_lives > 10:
        st.error("Remaining lives must be between 0 and 10.")
        return

    total_lives = 10
    used_lives = total_lives - remaining_lives

    colors = ["green" if remaining_lives > 0 else "gray", "red"]

    labels = ["Remaining Lives", "Used Lives"]

    data = [remaining_lives, used_lives]

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,
        colors=colors,
        autopct="%1.0f%%",
        startangle=90,
        wedgeprops={"edgecolor": "black"},
    )

    ax.add_artist(plt.Circle((0, 0), 0.7, color="white", fc="white"))

    plt.title(f"Lives Remaining: {remaining_lives}/{total_lives}")

    st.pyplot(fig)


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

st.title("🧙🏽DnD Adventure")

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

with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your action:", key="input", placeholder="What would you like to do?"
    )
    submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        with st.spinner("The Dungeon Master is thinking..."):
            dm_response = send_message(user_input)
            st.write(dm_response)
