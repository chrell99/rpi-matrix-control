from bottle import Bottle, static_file, template, run
import os
import argparse

from thumbnails import generate_thumbnails

def parse_args():
    parser = argparse.ArgumentParser(
        description="Media Launcher Web App"
    )
    parser.add_argument(
        '--media-folder',
        default=os.path.expanduser("~/media"),
        help='Media folder (default: ~/media)'
    )
    parser.add_argument(
        '--thumb-folder',
        default=os.path.expanduser("~/thumbnails"),
        help='Thumbnail folder (default: ~/thumbnails)'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port (default: 8080)'
    )
    parser.add_argument(
        '--generate-thumbs',
        action='store_true',
        help='Generate missing thumbnails on startup'
    )
    return parser.parse_args()

def create_app(media_folder, thumb_folder):
    app = Bottle()

    @app.route('/static/<filename:path>')
    def serve_static(filename):
        return static_file(filename, root='static')

    @app.route('/media/<filename:path>')
    def serve_media(filename):
        return static_file(filename, root=media_folder)

    @app.route('/thumbnails/<filename:path>')
    def serve_thumb(filename):
        return static_file(filename, root=thumb_folder)

    @app.route('/')
    def index():
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
    <link rel="stylesheet" href="/static/style.css">
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

    return app

if __name__ == "__main__":
    args = parse_args()

    if args.generate_thumbs:
        generate_thumbnails(args.media_folder, args.thumb_folder)

    app = create_app(args.media_folder, args.thumb_folder)
    run(app, host=args.host, port=args.port, debug=True)
