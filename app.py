import os
import json
from bottle import Bottle, request, static_file, run, TEMPLATE_PATH

# Pin process to CPU core 0 (cores are zero-indexed)
os.sched_setaffinity(0, {0})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH.clear()
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'templates'))

BRIGHTNESS = 100

from services.thumbnails import generate_thumbnails
from services.rpi_led_matrix import stop_running_process, start_strobe
from services.settings import set_setting, get_setting
from services.configs import load_config
from services.streams import start_background_processor
from routes.mediaControl import setup_mediaControl
from routes.index import setup_index
from routes.strobe import setup_strobe
from routes.mediaUpload import setup_mediaUpload

CONFIG_FILE = 'config.json'

def create_app(media_folder, thumb_folder, stream_folder):
    app = Bottle()

    # Serve files from /static folder
    @app.route('/static/<filepath:path>')
    def serve_static(filepath):
        return static_file(filepath, root=os.path.join(BASE_DIR, 'static'))

    # Serve thumbnails from /thumbnails folder
    @app.route('/thumbnails/<filepath:path>')
    def serve_thumbnails(filepath):
        return static_file(filepath, root=thumb_folder)
    
    # Serve media from /media folder
    @app.route('/media/<filepath:path>')
    def serve_media(filepath):
        return static_file(filepath, root=media_folder)
    
    @app.post('/stop_media')
    def stop_media():
        stop_running_process()

    @app.post('/set_brightness')
    def set_brightness():
        print(request.json)
        data = request.json
        new_level = data.get('brightness')

        if new_level is not None:
            set_setting("brightness", new_level)
            return {"status": "success", "value": new_level}
        else:
            return {"status": "error", "message": "Invalid data"}
        
    @app.post('/default_strobe')
    def default_strobe():
        on_time = get_setting("strobe_settings.on_time_ms")
        off_time = get_setting("strobe_settings.off_time_ms")
        brightness = get_setting("strobe_settings.brightness")

        start_strobe(on_time, off_time, brightness)

    setup_index(app)

    setup_mediaControl(app, media_folder, thumb_folder, stream_folder)

    setup_strobe(app)

    setup_mediaUpload(app, media_folder, thumb_folder)

    return app

if __name__ == "__main__":
    config = load_config()
    start_background_processor()

    if config.get("generate_thumbs"):
        generate_thumbnails(config["media_folder"], config["thumb_folder"])

    print(f"media path: {config["media_folder"]}, Thumb path: {config["thumb_folder"]}, Streams path {config["stream_folder"]}")

    app = create_app(config["media_folder"], config["thumb_folder"], config["stream_folder"])
    run(app, host=config.get("host", "0.0.0.0"), port=config.get("port", 8080), debug=True)
