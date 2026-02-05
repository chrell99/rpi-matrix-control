import os
from bottle import template, request
from services.rpi_led_matrix import start_videoviewer

def setup_mediaControl(app, media_folder, thumb_folder):
    @app.route('/mediaControl')
    def mediaControl():
        media_files = [
            f for f in os.listdir(media_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))
        ]

        display_items = []
        for f in media_files:
            if f.lower().endswith(('.mp4', '.webm')):
                base = os.path.splitext(f)[0]
                thumb = base + ".png"
                if not os.path.exists(os.path.join(thumb_folder, thumb)):
                    thumb = "placeholder.png"
                display_items.append({'type': 'video', 'file': f, 'thumb': thumb})
            else:
                display_items.append({'type': 'image', 'file': f})

        return template('mediaControl.html', display_items=display_items)
    
    @app.post('/run-media')
    def run_media():
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
