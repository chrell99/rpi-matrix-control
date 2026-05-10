import os
from bottle import template, request
from services.rpi_led_matrix import start_name_picker
from services.settings import _load_all

def setup_namePicker(app):
    @app.route('/namePicker')
    def namePicker():
        all_settings = _load_all()
        return template('namePicker.html', settings=all_settings)
        
    @app.post('/trigger_namePicker')
    def trigger_musicsync():
        try:
            start_name_picker()
            return f"Started name picker"
        except Exception as e:
            return f"Error: {str(e)}"
        