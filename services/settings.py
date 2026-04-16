import json
import os
from threading import Lock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.abspath(os.path.join(BASE_DIR, '../settings.json'))
file_lock = Lock()

def _load_all():
    if not os.path.exists(SETTINGS_FILE):
        print("Could not find the file settings.json")
    
    with open(SETTINGS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("error while json decoding the settings file")

def update_setting(key, value):
    with file_lock:
        data = _load_all()
        data[key] = value
        
        temp_file = SETTINGS_FILE + ".tmp"
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        os.replace(temp_file, SETTINGS_FILE)

def get_setting(key):
    with file_lock:
        data = _load_all()
        return data.get(key)