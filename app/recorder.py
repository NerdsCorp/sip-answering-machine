import sounddevice as sd
import soundfile as sf
import os
from datetime import datetime

def record_message(duration, filename):
    fs = 44100
    print(f"Recording message for {duration} seconds.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    if not os.path.exists("recordings"):
        os.makedirs("recordings")
    file_path = f"recordings/{filename}"
    sf.write(file_path, recording, fs)
    return file_path
