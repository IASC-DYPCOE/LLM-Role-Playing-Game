# Dungeons & Dragons RPG Chat 🎲📜🧙‍♂️

Embark on an interactive Dungeons & Dragons (DnD) adventure with a fully immersive chatbot experience. This project combines **FastAPI**, **Streamlit**, and **Google’s Gemini LLM** to create a Dungeon Master (DM) that guides players through a text-based DnD game. 🤖✨

---

## Features 🛡️⚔️📜
- **Interactive Gameplay**: Role-play as a DnD adventurer guided by an AI-powered Dungeon Master.
- **Dynamic Storytelling**: Experience evolving storylines and events based on your choices.
- **Custom Backend**: Built with FastAPI for robust handling of game logic and communication.
- **Handcrafted Prompts**: Carefully designed prompts ensure immersive and coherent narratives.
- **Streamlit Frontend**: A sleek, real-time chat interface for seamless player interaction.

---

## Technologies Used 🛠️🌐✨

- **FastAPI**: Backend framework for managing game logic and API endpoints.
- **Streamlit**: Frontend for interactive gameplay.
- **Google Gemini LLM**: Powers the AI Dungeon Master for natural and creative storytelling.
- **Requests**: Handles HTTP requests between the frontend and backend.
- **Python**: Core programming language for the project.

---

## Requirements 📦🖥️⚙️

### Python Libraries
Ensure you have the following Python libraries installed:
- `fastapi`
- `streamlit`
- `requests`
- `pydantic`
- `dotenv`
- `google`

Install them using:
```bash
pip install fastapi streamlit requests pydantic python-dotenv google
```

### Hardware
- A computer with an active internet connection.

---

## How It Works 🧙‍♀️📖🎲

1. **Backend (FastAPI)**:
   - Hosts endpoints to manage game state.
   - Initializes the global chat history and sends input to Google Gemini LLM for responses.

2. **Frontend (Streamlit)**:
   - Provides a user-friendly chat interface for gameplay.
   - Displays the Dungeon Master’s responses and allows players to input their actions.

3. **Game Logic**:
   - The backend maintains a global chat history for continuity.
   - Inputs from the player are processed, and the Dungeon Master responds with contextually relevant actions or story progressions.

---

## How to Run 🚀🎮📜

### Backend Setup
1. Start the FastAPI server:
   ```bash
   python -m uvicorn main:app --reload
   ```
   
   - This runs the backend at `http://127.0.0.1:8000/`.

### Frontend Setup
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

   - The Streamlit interface will launch in your default browser.

### Starting the Game
3. In the Streamlit app:
   - Click on **Start New Game** to initialize the adventure.
   - Enter your actions in the text input box and interact with the Dungeon Master.

---

## API Endpoints 📡✨🌐

### `/dnd/start` (GET)
- **Description**: Initializes the game by setting up the global chat history and starting the storyline.
- **Response**: Returns the initial narrative from the Dungeon Master.

### `/dnd/play` (POST)
- **Description**: Processes the player’s action and returns the Dungeon Master’s response.
- **Request Body**:
  ```json
  {
    "input_text": "<Player's action>"
  }
  ```
- **Response**: Returns the next part of the adventure.

---

## Key Modules 🔑📜✨

### `DuengeonMaster` Class
- Manages chat history and communicates with the Google Gemini LLM.
- **Methods**:
  - `set_global_chat_history(chat_history)`: Initializes or updates the global chat history.
  - `inference(input_text)`: Sends player input to the LLM and returns its response.

### FastAPI Endpoints
- `@app.get("/dnd/start")`: Handles game initialization.
- `@app.post("/dnd/play")`: Processes player input and returns a response.

### Streamlit Frontend
- Initializes session state for chat history.
- Displays player and Dungeon Master messages in an intuitive interface.

---

## Future Improvements 🌟📈🚀
- Add support for multi-player mode.
- Include visual elements like maps or character portraits.
- Improve prompt engineering for richer storytelling.
- Support saving and loading game progress.

---

## Acknowledgments 🤝🎉📚
- **FastAPI** for the backend framework.
- **Streamlit** for the interactive frontend.
- **Google Gemini LLM** for providing advanced AI capabilities.
- The DnD community for inspiration and guidance. 🎲🛡️⚔️

