import os
import json
from bottle import Bottle, static_file, run, TEMPLATE_PATH

# Pin process to CPU core 0 (cores are zero-indexed)
os.sched_setaffinity(0, {0})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH.clear()
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'templates'))


from services.thumbnails import generate_thumbnails
from services.rpi_led_matrix import stop_running_process
from routes.mediaControl import setup_mediaControl
from routes.index import setup_index
from routes.strobe import setup_strobe

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
        return static_file(filepath, root=os.path.join(BASE_DIR, 'static'))

    # Serve thumbnails from /thumbnails folder
    @app.route('/thumbnails/<filepath:path>')
    def serve_thumbnails(filepath):
        return static_file(filepath, root=os.path.join(BASE_DIR, '..', 'thumbnails'))
    
    # Serve media from /media folder
    @app.route('/media/<filepath:path>')
    def serve_media(filepath):
        return static_file(filepath, root=os.path.join(BASE_DIR, '..', 'media'))
    
    @app.post('/stop_media')
    def stop_media():
        stop_running_process()

    setup_index(app)

    setup_mediaControl(app, media_folder, thumb_folder)

    setup_strobe(app)

    return app

if __name__ == "__main__":
    config = load_config()

    if config.get("generate_thumbs"):
        generate_thumbnails(config["media_folder"], config["thumb_folder"])

    app = create_app(config["media_folder"], config["thumb_folder"])
    run(app, host=config.get("host", "0.0.0.0"), port=config.get("port", 8080), debug=True)
