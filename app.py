from bottle import Bottle, static_file, template, run
import os
import json

from services.thumbnails import generate_thumbnails
from routes.mediaControl import setup_mediaControl

CONFIG_FILE = 'config.json'

def load_config(path=CONFIG_FILE):
    if not os.path.exists(path):
        # default values if config file is missing
        return {
            "media_folder": os.path.expanduser("~/media"),
            "thumb_folder": os.path.expanduser("~/thumbnails"),
            "host": "0.0.0.0",
            "port": 8080,
            "generate_thumbs": False
        }

    with open(path, 'r') as f:
        return json.load(f)

def create_app(media_folder, thumb_folder):
    app = Bottle()

    # Serve files from /static folder
    @app.route('/static/<filepath:path>')
    def serve_static(filepath):
        return static_file(filepath, root='static')

    @app.route('/test')
    def test():
        return "Hello world!"

    setup_mediaControl(app, media_folder, thumb_folder)

    return app

if __name__ == "__main__":
    config = load_config()

    if config.get("generate_thumbs"):
        generate_thumbnails(config["media_folder"], config["thumb_folder"])

    app = create_app(config["media_folder"], config["thumb_folder"])
    run(app, host=config.get("host", "0.0.0.0"), port=config.get("port", 8080), debug=True)
