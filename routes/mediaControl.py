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

        return template('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>rpi-matrix-control</title>
                <link rel="stylesheet" href="/static/css/style.css">
                <link rel="icon" type="image/x-icon" href="/static/images/hoolacane-logo.ico">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
            <main class="grid">
            % for item in display_items:
                <button class="media-item" data-file="{{item['file']}}">
                    % if item['type'] == 'video':
                        <img src="/thumbnails/{{item['thumb']}}">
                    % else:
                        <img src="/media/{{item['file']}}">
                    % end
                </button>
            % end
            </main>
            </body>
            </html>
        ''', display_items=display_items)