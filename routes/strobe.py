import os
from bottle import template, request
from services.rpi_led_matrix import start_videoviewer

def setup_strobe(app):
    @app.route('/strobe')
    def strobe():
        return template('strobe.html')
    
    @app.post('/run-strobe')
    def run_strobe():
        data = request.json
        filename = data.get('file')
        if not filename:
            return "No file specified"
        
        filename_no_ext, _ = os.path.splitext(filename)

        try:
            start_videoviewer(filename_no_ext)
            return f"Started {filename_no_ext}"
        except Exception as e:
            return f"Error: {str(e)}"
