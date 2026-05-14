import os
from bottle import template, request
from services.rpi_led_matrix import start_roulette
from services.settings import _load_all

def setup_roulette(app):
    @app.route('/roulette')
    def roulette():
        all_settings = _load_all()
        return template('roulette.html', settings=all_settings)
        
    @app.post('/trigger_roulette')
    def trigger_roulette():
        try:
            start_roulette()
            return f"Started roulette"
        except Exception as e:
            return f"Error: {str(e)}"
        