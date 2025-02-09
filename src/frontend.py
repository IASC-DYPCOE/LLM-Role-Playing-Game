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
if "game_started" not in st.session_state:
    st.session_state.game_started = False

st.set_page_config(
    page_title="Realm of Adventures", 
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with Medieval Theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url("https://images.unsplash.com/photo-1599058917212-d6f5e99e4946") no-repeat center center fixed;
        background-size: cover;
    }
    
    .title-container {
        text-align: center;
        padding: 2rem;
        background: rgba(51, 25, 0, 0.8);
        border-radius: 15px;
        border: 2px solid #8B4513;
        margin-bottom: 2rem;
    }
    
    .game-title {
        font-family: 'MedievalSharp', cursive;
        color: #FFD700;
        font-size: 3rem;
        text-shadow: 2px 2px 4px #000;
    }
    
    .message-container {
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(77, 45, 45, 0.9), rgba(100, 50, 50, 0.9));
        text-align: right;
        margin-left: 20%;
        border-left: 4px solid #FFD700;
        color: #FFE5B4;
    }
    
    .dm-message {
        background: linear-gradient(135deg, rgba(40, 40, 40, 0.95), rgba(30, 30, 30, 0.95));
        margin-right: 20%;
        border-right: 4px solid #4A90E2;
        color: #E0C097;
    }
    
    .chat-container {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        padding: 20px;
        max-height: 600px;
        overflow-y: auto;
        margin-bottom: 2rem;
        border: 1px solid #8B4513;
    }
    
    .typing-animation {
        color: #FFD700;
        font-family: 'MedievalSharp', cursive;
        font-size: 1.2rem;
        text-align: center;
    }
    
    .stButton>button {
        background-color: #8B4513;
        color: #FFD700;
        font-family: 'MedievalSharp', cursive;
        border: 2px solid #FFD700;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #A0522D;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #FFD700;
        border: 2px solid #8B4513;
        border-radius: 8px;
        padding: 0.8rem;
        font-family: 'MedievalSharp', cursive;
    }
    
    .stats-container {
        background: rgba(51, 25, 0, 0.8);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #8B4513;
        margin-top: 1rem;
    }
    
    .stat-value {
        font-size: 1.5rem;
        color: #FFD700;
        text-align: center;
        font-family: 'MedievalSharp', cursive;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title Section
st.markdown(
    """
    <div class="title-container">
        <h1 class="game-title">🐉 Realm of Adventures 🗡️</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Game Functions
def start_new_game():
    st.session_state.chat_history = []
    st.session_state.dm = DungeonMaster()
    st.session_state.game_started = True
    response = st.session_state.dm.inference(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "dm", "content": response})
    return response

def typewriter_effect(text: str, placeholder) -> None:
    """Display text with typewriter effect while preserving formatting"""
    full_text = ""
    # Split into paragraphs first
    paragraphs = text.split('\n')
    
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():  # If paragraph isn't empty
            words = paragraph.split()
            for word in words:
                full_text += word + " "
                placeholder.markdown(
                    f'<div class="message-container dm-message">🧙‍♂️ {full_text}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.1)
        
        # Add newline between paragraphs if it's not the last paragraph
        if i < len(paragraphs) - 1:
            full_text += "\n\n"
            placeholder.markdown(
                f'<div class="message-container dm-message">🧙‍♂️ {full_text}</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.1)

def send_message(message: str) -> str:
    response = st.session_state.dm.inference(st.session_state.chat_history, message)
    st.session_state.chat_history.append({"role": "user", "content": message})
    st.session_state.chat_history.append({"role": "dm", "content": response})
    st.rerun()  # Changed from experimental_rerun to rerun
    return response

# Game Layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    if not st.session_state.game_started:
        if st.button("⚔️ Begin Your Adventure ⚔️"):
            with st.spinner("🎲 The ancient scrolls are unfolding..."):
                game_response = start_new_game()

    # Chat Container
    chat_container = st.container()
    
    # User Input (Moved above chat display)
    if st.session_state.game_started:
        with st.form(key="message_form", clear_on_submit=True):
            user_input = st.text_input(
                "Your next move:", 
                key="input", 
                placeholder="What actions shall you take, brave adventurer?"
            )
            submit_button = st.form_submit_button("🗣️ Declare Your Action")
            
            if submit_button and user_input.strip():
                typing_placeholder = st.empty()
                for i in range(3):
                    typing_placeholder.markdown(
                        f'<p class="typing-animation">{"." * (i + 1)} The Dungeon Master contemplates {"." * (i + 1)}</p>',
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.4)
                
                dm_response = send_message(user_input)
                typing_placeholder.empty()
                
                # Update turns remaining
                turns = extract_lives_remaining(dm_response)
                st.session_state.current_turns = turns
    
    # Chat Display (Moved below input)
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for i, message in enumerate(st.session_state.chat_history[:-1]):  # All messages except the last one
            if message["role"] == "user":
                st.markdown(
                    f'<div class="message-container user-message">🧝‍♂️ {message["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="message-container dm-message">🧙‍♂️ {message["content"]}</div>',
                    unsafe_allow_html=True,
                )
        
        # Handle the last message with typewriter effect if it's from DM
        if st.session_state.chat_history:
            last_message = st.session_state.chat_history[-1]
            if last_message["role"] == "user":
                st.markdown(
                    f'<div class="message-container user-message">🧝‍♂️ {last_message["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                message_placeholder = st.empty()
                typewriter_effect(last_message["content"], message_placeholder)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats Display (Below chat)
    if st.session_state.game_started and hasattr(st.session_state, 'current_turns'):
        st.markdown(
            f"""
            <div class="stats-container">
                <div class="stat-value">⌛ Turns Remaining: {st.session_state.current_turns}</div>
            </div>
            """,
            unsafe_allow_html=True
        )