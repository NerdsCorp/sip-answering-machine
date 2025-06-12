import subprocess
import threading
import time
import os
from app.config_manager import load_config
from app.notifier import send_to_discord, send_email

def monitor_baresip():
    config = load_config()
    config_dir = os.path.abspath(config['baresip_config_dir'])
    recording_path = config['recording_path']

    # Start baresip process
    process = subprocess.Popen(["baresip", "-f", config_dir],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    print("Baresip started. Monitoring logs...")

    for line in iter(process.stdout.readline, b''):
        decoded_line = line.decode().strip()
        print(decoded_line)

        if "incoming call from" in decoded_line:
            print("Call received — autoanswer enabled.")

        if "call closed" in decoded_line:
            print("Call ended — sending recording.")
            if os.path.exists(recording_path):
                send_to_discord(recording_path)
                send_email(recording_path)
            else:
                print("No recording file found.")

def start_baresip_monitor():
    thread = threading.Thread(target=monitor_baresip)
    thread.start()
