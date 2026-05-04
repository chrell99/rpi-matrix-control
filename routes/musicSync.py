import os
from bottle import template, request
from services.rpi_led_matrix import start_strobe_to_beat, start_spectrum_visualizer

def setup_musicsync(app):
    @app.route('/musicsync')
    def musicsync():
        return template('musicSync.html')
        
    @app.post('/trigger_musicsync')
    def trigger_musicsync():
        data = request.json
        app_id = data.get('app_id')
        
        if app_id == 'strobe_to_beat':
            try:
                start_strobe_to_beat()
                return f"Started strobe_to_beat"
            except Exception as e:
                return f"Error: {str(e)}"
            
        elif app_id == 'spectrum_visualizer':
            try:
                start_spectrum_visualizer()
                return f"Started spectrum_visualizer"
            except Exception as e:
                return f"Error: {str(e)}"