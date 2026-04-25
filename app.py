from flask import Flask, send_from_directory, jsonify, Response
import subprocess
import threading
import queue
import sys
import os
import re

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\[[?0-9;]*[a-zA-Z]|\r')

app = Flask(__name__, static_folder='.', static_url_path='')

log_queue = queue.Queue()
assistant_process = None

def run_assistant():
    global assistant_process
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    assistant_process = subprocess.Popen(
        [sys.executable, "-u", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',
        env=env
    )
    
    for line in iter(assistant_process.stdout.readline, ''):
        if line:
            clean = ANSI_ESCAPE.sub('', line).strip()
            if clean and not all(c in ' \t\n\r' for c in clean):
                log_queue.put(clean)
            
    assistant_process.stdout.close()
    assistant_process.wait()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/start', methods=['POST'])
def start():
    global assistant_process
    if assistant_process and assistant_process.poll() is None:
        return jsonify({"status": "already running"})
    
    thread = threading.Thread(target=run_assistant)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    global assistant_process
    if assistant_process and assistant_process.poll() is None:
        assistant_process.terminate()
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not running"})

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            # Block until a log line is available
            line = log_queue.get()
            # Send the line as a server-sent event (SSE)
            yield f"data: {line}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    print("Starting Web Server. Open http://127.0.0.1:5000 in your browser.")
    app.run(port=5000)
