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
            # Only proceed if the key was actually sent in the POST request
            if key in request.forms:
                new_value = request.forms.get(key)
                
                # Fix encoding if necessary
                if new_value:
                    try:
                        new_value = new_value.encode('latin-1').decode('utf-8')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        pass 

                # Handle List types (CSV to List)
                if isinstance(current_value, list):
                    # Ensure we handle empty strings for lists gracefully
                    processed_value = [item.strip() for item in new_value.split(',') if item.strip()]
                    set_setting(key, processed_value)
                else:
                    # Handle standard types
                    set_setting(key, new_value)
                    
        return redirect('/settings')