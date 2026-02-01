import os
from bottle import template

def setup_index(app):
    @app.route('/')
    def home():
        return template('''
            % rebase('base.html', title="Home")
            <div class="grid">
                <button onclick="location.href='/mediaControl'">Media Control</button>
                <button onclick="location.href='/config'">Settings / Config</button>
            </div>
        ''')