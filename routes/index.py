from bottle import template

def setup_index(app):
    @app.route('/')
    def home():
        return template('index.html')