import os
from bottle import template, request
from services.rpi_led_matrix import start_strobe

def setup_strobe(app):
    @app.route('/strobe')
    def strobe():
        return template('strobe.html')
    
    @app.post('/run-strobe')
    def run_strobe():
        data = request.json

        if not data:
            return "No JSON payload received"

        try:
            on_time = int(data.get('on_time'))
            off_time = int(data.get('off_time'))
            brightness = int(data.get('brightness'))

            # Optional safety checks
            if on_time <= 0 or off_time <= 0:
                return "Invalid timing values"

            if not (0 <= brightness <= 100):
                return "Brightness out of range"

            # Call your hardware logic
            start_strobe(
                on_time=on_time,
                off_time=off_time,
                brightness=brightness
            )

            return {
                "status": "ok",
                "on_time": on_time,
                "off_time": off_time,
                "brightness": brightness
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
