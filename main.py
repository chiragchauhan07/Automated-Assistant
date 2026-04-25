import speech_recognition as sr
import subprocess
import edge_tts
import asyncio
import os
import tempfile
import playsound
import webbrowser
import re
import json
import pyautogui
import time
# ================= CONFIG =================

VOICE = "en-US-GuyNeural"
OLLAMA_MODEL = "mistral:latest"
OLLAMA_PATH = r"C:\Users\LENOVO\AppData\Local\Programs\Ollama\ollama.exe"

USER_HOME = os.path.expanduser("~")
PROJECT_DIR = os.path.join(USER_HOME, "AssistantProjects")
os.makedirs(PROJECT_DIR, exist_ok=True)

# ================= APP MAPS ================
 
SYSTEM_APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "calculator": "calc",
    "task manager": "taskmgr",
    "control panel": "control",
    "command prompt": "cmd",
    "powershell": "powershell",
    "notepad": "notepad",
    "file explorer": "explorer",
    "explorer": "explorer",
    "settings": "ms-settings:",
    "vs code": "code",
    "visual studio code": "code",
}

STORE_APPS = {
    "whatsapp": "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
    "spotify": "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify",
}

FOLDERS = {
    "documents": os.path.join(USER_HOME, "Documents"),
    "downloads": os.path.join(USER_HOME, "Downloads"),
    "desktop": os.path.join(USER_HOME, "Desktop"),
    "pictures": os.path.join(USER_HOME, "Pictures"),
    "music": os.path.join(USER_HOME, "Music"),
    "videos": os.path.join(USER_HOME, "Videos"),
}

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "netflix": "https://www.netflix.com",
    "google": "https://www.google.com",
}

LANG_EXTENSIONS = {
    "python": "py",
    "java": "java",
    "javascript": "js",
    "html": "html",
    "css": "css",
    "cpp": "cpp",
    "c plus plus": "cpp",
    "text": "txt",
}

#SPEAK

async def speak_async(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        path = f.name
    await edge_tts.Communicate(text, VOICE).save(path)
    playsound.playsound(path)
    os.remove(path)

def speak(text):
    asyncio.run(speak_async(text))

#LISTEN 

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.6

    with sr.Microphone() as source:
        print("[MIC] Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return ""

# AI THINK
def think(prompt, code_mode=False):
    try:
        process = subprocess.Popen(
            ["ollama", "run", OLLAMA_MODEL],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if code_mode:
            system_prompt = (
                "You are a code generator.\n"
                "Output ONLY valid source code.\n"
                "DO NOT explain.\n"
                "DO NOT use markdown.\n"
                "DO NOT include backticks.\n"
                "DO NOT include comments unless asked.\n"
                "If asked to write code, output code only.\n\n"
            )
        else:
            system_prompt = (
                "You are an advanced, highly intelligent, and friendly voice assistant named Automated Assistant.\n"
                "Your goal is to provide smooth, professional, and accurate responses.\n"
                "Keep your answers helpful but concise (1-3 sentences).\n"
                "Speak naturally as if you are a real person.\n"
                "DO NOT use markdown, emojis, or symbols.\n"
                "DO NOT output code unless specifically asked.\n"
                "Respond in a single paragraph of plain text only.\n\n"
            )

        stdout, stderr = process.communicate(system_prompt + prompt)

        if code_mode:
            return clean_code(stdout)
        else:
            # Remove any internal newlines to keep the output on a single line
            return " ".join(stdout.split()).strip() if stdout else ""

    except Exception as e:
        print("Think error:", e)
        return ""

def clean_code(text):
    if not text:
        return ""

    lines = text.splitlines()
    cleaned = []

    for line in lines:
        if line.strip().startswith(("```", "Here", "This code", "Explanation")):
            continue
        cleaned.append(line)

    return "\n".join(cleaned).strip()


def ai_write_code_to_file(prompt, filename):
    try:
        raw = think(code_mode=True, prompt=f"""
You are a compiler, not a teacher.

RULES (MANDATORY):
- Output ONLY executable code
- NO explanations
- NO markdown
- NO triple backticks
- NO comments unless required by syntax
- Start directly with code

TASK:
{prompt}
"""
        )

        if not raw or not raw.strip():
            speak("No code generated.")
            return

        #  HARD CLEANUP
        lines = raw.splitlines()
        clean_lines = []

        for line in lines:
            if line.strip().startswith("```"):
                continue
            if line.lower().startswith("here"):
                continue
            if line.lower().startswith("to create"):
                continue
            if line.lower().startswith("when you run"):
                continue
            clean_lines.append(line)

        code = "\n".join(clean_lines).strip()

        if not code:
            speak("AI response was invalid.")
            return

        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)

        speak(f"Code written to {filename}")

    except Exception as e:
        print("Code write error:", e)
        speak("Failed to write code.")

def explain_code_file(filename):
    if not os.path.exists(filename):
        speak(f"I cannot find the file {filename}")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        prompt = (
            "Explain the following code clearly and briefly:\n\n"
            + code
        )

        explanation = think(prompt)

        if not explanation:
            explanation = "I could not generate an explanation."

        print("Automated Assistant:", explanation)
        speak(explanation)

    except Exception as e:
        speak("I encountered an error while reading the file.")

#  INTENT 

def classify_intent(text):
    if any(w in text for w in ["open", "start", "launch"]):
        return "action"
    if "create" in text and "file" in text:
        return "create_file"
    if any(w in text for w in ["code", "program", "script", "write"]):
        return "code"
    return "question"

#  ACTION HANDLER 

def handle_open(text):
    if text in FOLDERS:
        subprocess.Popen(["explorer", FOLDERS[text]])
        return True

    if text in SYSTEM_APPS:
        subprocess.Popen(SYSTEM_APPS[text], shell=True)
        return True

    if text in STORE_APPS:
        subprocess.Popen(f'explorer "{STORE_APPS[text]}"', shell=True)
        return True

    if text in WEBSITES:
        webbrowser.open(WEBSITES[text])
        return True

    return False

#  FILE CREATION 

def extract_filename(text):
    text = text.replace("dot", ".")
    direct = re.search(r"\b([\w\-]+\.[a-z0-9]+)\b", text)
    if direct:
        return direct.group(1)

    for lang, ext in LANG_EXTENSIONS.items():
        if lang in text:
            m = re.search(r"name\s+([\w\-]+)", text)
            if m:
                return f"{m.group(1)}.{ext}"

    return None

def create_file(filename):
    path = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8"):
            pass
    subprocess.Popen(["code", path], shell=True)
    speak(f"{filename} created and opened.")

def create_code_file(user_input):
    filename = extract_filename(user_input)
    if not filename:
        speak("Please tell me the file name.")
        return

    prompt = f"Write complete code only.\nTask:\n{user_input}"
    code = think(prompt, code_mode=True)

    if not code:
        speak("I could not generate the code.")
        return

    path = os.path.join(PROJECT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    subprocess.Popen(["code", path], shell=True)
    speak(f"{filename} created with code.")

def google_search(query):
    speak(f"Searching Google for {query}")
    query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    subprocess.Popen(["cmd", "/c", "start", url])

# ===================== WHATSAPP PARSER =====================
def parse_whatsapp_command(text):
    """
    Extracts (contact, message) from:
    'send whatsapp message to papa ji what are you doing'
    """

    text = text.lower()

    if "send whatsapp message to" not in text:
        return None, None

    after_to = text.split("send whatsapp message to", 1)[1].strip()
    words = after_to.split()

    # words that usually start a message
    message_starters = {
        "what", "how", "where", "when",
        "call", "tell", "say", "please",
        "are", "is", "can", "do"
    }

    contact_words = []
    message_words = []

    found_message = False
    for word in words:
        if not found_message and word in message_starters:
            found_message = True

        if found_message:
            message_words.append(word)
        else:
            contact_words.append(word)

    contact = " ".join(contact_words).strip()
    message = " ".join(message_words).strip()

    if not contact:
        return None, None

    if not message:
        message = "Hello"

    return contact, message
 

# ===================== WHATSAPP SENDER (FIXED) =====================
def send_whatsapp_message(contact, message):
    """
    FINAL WhatsApp sender
    No recursion
    No parsing
    No side effects
    """

    if not contact:
        speak("Contact name missing.")
        return

    if not message:
        speak(f"What message should I send to {contact}?")
        return

    # Open WhatsApp Desktop
    subprocess.Popen(
        f'explorer "{STORE_APPS["whatsapp"]}"',
        shell=True
    )

    time.sleep(6)

    # Search contact
    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)
    pyautogui.typewrite(contact, interval=0.05)
    time.sleep(2)
    pyautogui.press("enter")

    time.sleep(1)
    pyautogui.typewrite(message, interval=0.03)
    pyautogui.press("enter")

    speak(f"Message sent to {contact}")

    


#  MAIN 

def main():
    speak("Automated Assistant version three is online.")

    while True:
        contact = None
        message = None

        user_input = listen()
        if not user_input:
            speak("I didn't catch that.")
            continue

        if any(w in user_input for w in ["stop", "exit", "shutdown"]):
            speak("Goodbye.")
            break

        intent = classify_intent(user_input)

        if intent == "action":
            target = user_input.replace("open", "").strip()
            if not handle_open(target):
                speak("I could not open that.")
            continue

        if intent == "create_file":
            filename = extract_filename(user_input)
            if filename:
                create_file(filename)
            else:
                speak("Please say the file name.")
            continue

        if intent == "code":
            create_code_file(user_input)
            continue

                # ---------- GOOGLE SEARCH ----------
        if user_input.startswith("search "):
            search_query = user_input.replace("search ", "").strip()
            if search_query:
                google_search(search_query)
                continue
                
             # WHATSAPP
        contact, message = parse_whatsapp_command(user_input)
        if contact:
            send_whatsapp_message(contact, message)
            continue


        #  AI CODE WRITING 
        if "write" in user_input and "file" in user_input:
            # Example: "write python code in test.py"
            words = user_input.split()

            filename = None
            for w in words:
                if "." in w:
                    filename = w
                    break

            if not filename:
                speak("Please tell me the file name.")
                continue

            ai_write_code_to_file(user_input, filename)
            continue

        if "explain" in user_input and ".py" in user_input:
            filename = user_input.split()[-1]
            explain_code_file(filename)
            continue

        response = think(user_input)
        if not response:
            response = "I am thinking, but I could not generate a response."

        print("Automated Assistant:", response)
        speak(response)

if __name__ == "__main__":
    main()