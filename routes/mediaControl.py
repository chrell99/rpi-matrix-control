import os
from bottle import template

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