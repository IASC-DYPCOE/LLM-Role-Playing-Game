import streamlit as st
import requests
from typing import List, Dict
import json


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "Welcome, brave adventurer! I am your Dungeon Master. What would you like to do?",
            }
        ]


def send_message(message: str) -> Dict:
    """Send message to the DnD backend and get response"""
    try:
        response = requests.get(
            "http://localhost:8000/dnd",  
            data={"form_input_text": message},
        )
        return response.json()
    except Exception as e:
        st.error(f"Error communicating with DM: {str(e)}")
        return {"content": "Sorry, I encountered an error. Please try again."}


def main():
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
        }
        .user-message {
            background-color: #2D2D2D;
        }
        .dm-message {
            background-color: #383838;
        }
        .css-1qrvfrg {  /* Style for text input */
            background-color: #2D2D2D;
            color: white;
            border-color: #4D4D4D;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    initialize_session_state()

    st.title("🎲 DnD Adventure")

    chat_container = st.container()

    with chat_container:
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

        if submit_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.spinner("The Dungeon Master is thinking..."):
                dm_response = send_message(user_input)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": dm_response.get(
                            "content", "Something went wrong. Please try again."
                        ),
                    }
                )

            st.experimental_rerun()


if __name__ == "__main__":
    main()
