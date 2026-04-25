AI Automated Assistant

The AI Automated Assistant is a Python-based intelligent system that combines **voice interaction, system automation, and AI-powered reasoning** to perform real-world tasks efficiently. Unlike basic assistants that rely only on predefined commands, this project integrates a local large language model using Ollama with the Mistral, enabling more natural and context-aware responses.

---

Overview

This project was built to reduce the effort of performing repetitive desktop tasks and to explore how AI can enhance traditional automation systems. The assistant allows users to interact through voice or text and performs tasks intelligently based on the input.

It follows a structured pipeline:

* Takes user input (voice/text)
* Converts speech to text
* Identifies intent
* Executes tasks or processes via AI
* Responds using natural voice

---

Key Features

1. Voice Interaction

* Captures voice commands using `speech_recognition`
* Converts responses into speech using `edge-tts`
* Enables hands-free system control

2. AI-Powered Responses

* Uses local LLM via Ollama (Mistral model)
* Handles:

  * General queries
  * Logical reasoning
  * Coding-related tasks
* Provides concise and contextual answers

3. System & Application Control

* Open applications (Chrome, VS Code, Notepad, Calculator)
* Access folders (Documents, Downloads, Desktop)
* Open websites like YouTube, Google, Netflix

3. Code Generation & Analysis

* Generate code in multiple languages
* Save generated code into files automatically
* Read and explain existing Python files

4. Automation

* Send WhatsApp messages using `pyautogui`
* Perform Google searches
* Execute system-level commands

5. Web Dashboard

* Built using Flask
* Real-time logs using Server-Sent Events (SSE)
* Start/Stop assistant from UI
* Live monitoring interface

---

How It Works

The assistant follows a modular workflow:

1. **Input Layer**

   * Voice input captured and converted to text

2. **Processing Layer**

   * Intent classification using keyword + regex logic

3. **AI Layer**

   * Queries processed using Mistral via Ollama (for intelligent responses)

4. **Execution Layer**

   * Performs actions (open apps, automate tasks, generate code)

5. **Output Layer**

   * Response delivered via text-to-speech

---

#Tech Stack

### Backend

* Python 3.x
* Flask
* speech_recognition
* edge-tts
* pyautogui
* subprocess, threading

### AI

* Ollama (local LLM runtime)
* Mistral Model

### Frontend (Dashboard)

* HTML
* CSS
* JavaScript (SSE for real-time updates)

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Automated-Assistant.git
cd AI-Automated-Assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Download and install Ollama from:
https://ollama.com/

### 4. Pull Mistral Model

```bash
ollama pull mistral
```

### 5. Run the Project

```bash
python app.py
```

---

## 📸 Screenshots

Add screenshots of:

* Dashboard UI
* Terminal logs
* Assistant running

---

## 🧩 Core Functionalities

* `speak(text)` → Converts text to speech
* `listen()` → Captures voice input
* `think(prompt)` → AI processing using Mistral
* `classify_intent(text)` → Identifies user intent
* `handle_open(text)` → Opens apps/websites
* `ai_write_code_to_file()` → Generates code
* `send_whatsapp_message()` → Automates messaging

---

## ⚡ Challenges & Learnings

* Integrating voice input with real-time processing
* Managing local LLM setup and response handling
* Handling concurrency using threading
* Designing modular and scalable architecture

---

## 🔮 Future Improvements

* Advanced NLP-based intent classification
* Context memory for better conversations
* Cross-platform support
* GUI-based assistant interface
* API integrations

---

## 🎯 Why This Project Stands Out

* Combines **AI + Automation + Voice Interaction**
* Uses **local LLM (no API dependency)**
* Supports **code generation + real task execution**
* Demonstrates **end-to-end system design**

---

## 📬 Contact

* LinkedIn: Add your link
* GitHub: Add your profile

---

⭐ If you find this project useful, consider giving it a star.
