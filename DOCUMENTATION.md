# Jarvis V3: Automated Assistant Documentation

## Project Overview
**Jarvis V3** (Automated Assistant Version 3) is a sophisticated, voice-controlled AI assistant designed to automate desktop tasks, generate code, and provide intelligent conversational responses. It features a modern terminal-style web interface for monitoring and control.

---

## Technical Stack

### Backend
- **Language**: Python 3.x
- **Web Framework**: Flask (for the dashboard and log streaming)
- **Speech Recognition**: `speech_recognition` library (using Google Speech API)
- **Text-to-Speech (TTS)**: `edge-tts` (Microsoft Edge's high-quality neural voices)
- **AI Core**: **Ollama** running the **Mistral** model locally.
- **Automation**: `pyautogui` for UI interactions (e.g., WhatsApp automation)
- **Process Management**: `subprocess` and `threading` for running the assistant logic and streaming logs.

### Frontend
- **Structure**: Semantic HTML5
- **Styling**: Vanilla CSS (Terminal aesthetic with glassmorphism)
- **Logic**: Vanilla JavaScript (Server-Sent Events for real-time log streaming)

---

## Key Features

### 1. Voice Interaction
- **Listening**: Uses `speech_recognition` to capture and transcribe user commands.
- **Speaking**: Uses `edge-tts` for natural-sounding voice responses (`en-US-GuyNeural`).

### 2. Intelligent Conversations (AI Thinking)
- Integrated with **Ollama (Mistral)** to provide concise, professional, and friendly responses.
- Context-aware system prompts for both general inquiries and coding tasks.

### 3. Application & System Control
- **Open Apps**: Launch Chrome, VS Code, Notepad, Calculator, Task Manager, etc.
- **Open Folders**: Quick access to Documents, Downloads, Desktop, etc.
- **Websites**: Instant navigation to YouTube, Netflix, and Google.

### 4. Code Generation & Analysis
- **Write Code**: AI generates executable code (Python, Java, JS, etc.) and saves it directly to a file.
- **Explain Code**: AI reads existing `.py` files and provides a clear summary of the logic.
- **Project Directory**: Automatically manages files in the `AssistantProjects` folder.

### 5. Automation
- **WhatsApp Integration**: Sends messages to contacts via WhatsApp Desktop using `pyautogui` automation.
- **Google Search**: Performs hands-free web searches.

### 6. Web Dashboard
- Real-time terminal output streaming via SSE (Server-Sent Events).
- Control buttons to **Start** and **Stop** the assistant process.
- Elegant UI with auto-scrolling terminal logs.

---

## Core Functions (main.py)

| Function | Description |
| :--- | :--- |
| `speak(text)` | Converts text to speech using Edge TTS and plays it. |
| `listen()` | Listens for voice input and returns it as text. |
| `think(prompt, code_mode)` | Communicates with the Ollama Mistral model to get a response. |
| `classify_intent(text)` | Uses regex and keyword matching to determine the user's goal. |
| `handle_open(text)` | Maps keywords to system paths and opens the requested application. |
| `ai_write_code_to_file(prompt, filename)` | Generates clean code and writes it to a specified file. |
| `send_whatsapp_message(contact, message)` | Automates WhatsApp Desktop to search and send a message. |

---

## File Structure
- `main.py`: Core assistant logic, voice processing, and task execution.
- `app.py`: Flask web server providing the API and serving the frontend.
- `index.html`: The web dashboard interface.
- `style.css`: Styles for the terminal UI and animations.

---

## Setup & Requirements
1. **Ollama**: Must be installed and running with the `mistral` model downloaded (`ollama pull mistral`).
2. **Python Dependencies**:
   ```bash
   pip install flask speechrecognition edge-tts playsound pyautogui
   ```
3. **Environment**: Windows (as it uses Windows-specific paths and `pyautogui`).

---

*Documentation generated on April 25, 2026.*
