import json
import os

def load_config(path="config.json"):
    if not os.path.exists(path):
        return {
            "media_folder": "/home/hoolacane/media",
            "thumb_folder": "/home/hoolacane/thumbnails",
            "stream_folder": "/home/hoolacane/streams",
            "host": "0.0.0.0",
            "port": 8080,
            "generate_thumbs": False
        }
    with open(path, 'r') as f:
        return json.load(f)