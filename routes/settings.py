import os
from bottle import route, run, template, request, redirect
from services.settings import set_setting, get_setting, _load_all

def setup_settings(app):

    @app.route('/settings')
    def settings_page():
        all_settings = _load_all()
        return template("settings.html", settings=all_settings)

    @app.route('/settings/update', method='POST')
    def update_settings():
        all_settings = _load_all()
        
        for key, current_value in all_settings.items():
            new_value = request.forms.get(key)
            if new_value:
                try:
                    new_value = new_value.encode('latin-1').decode('utf-8')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass # Already UTF-8 or doesn't need fixing
            
            if isinstance(current_value, list):
                processed_value = [item.strip() for item in new_value.split(',') if item.strip()]
                set_setting(key, processed_value)
            else:
                set_setting(key, new_value)
                
        return redirect('/settings')