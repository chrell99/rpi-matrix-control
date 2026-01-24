from bottle import Bottle, static_file, template, run
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Simple Media Launcher Web App"
    )
    parser.add_argument(
        '--media-folder',
        default=os.path.expanduser("~/media"),
        help='Folder where media files are stored (default: ~/media)'
    )
    parser.add_argument(
        '--thumb-folder',
        default=os.path.expanduser("~/thumbnails"),
        help='Folder where thumbnail images are stored (default: ~/thumbnails)'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to run the server on (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to run the server on (default: 8080)'
    )
    return parser.parse_args()

def create_app(media_folder, thumb_folder):
    # Ensure folders exist
    os.makedirs(media_folder, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)

    app = Bottle()

    # Serve static files
    @app.route('/static/<filename:path>')
    def serve_static(filename):
        return static_file(filename, root='static')

    # Serve media files
    @app.route('/media/<filename:path>')
    def serve_media(filename):
        return static_file(filename, root=media_folder)

    # Serve thumbnails
    @app.route('/thumbnails/<filename:path>')
    def serve_thumb(filename):
        return static_file(filename, root=thumb_folder)

    @app.route('/')
    def index():
        media_files = os.listdir(media_folder)
        media_files = [f for f in media_files if f.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))]

        display_items = []
        for f in media_files:
            if f.lower().endswith(('.mp4', '.webm')):
                # Use corresponding thumbnail if it exists
                base_name = os.path.splitext(f)[0]
                thumb_file = base_name + ".png"
                if not os.path.exists(os.path.join(thumb_folder, thumb_file)):
                    thumb_file = "placeholder.png"
                display_items.append({'type': 'video', 'file': f, 'thumb': thumb_file})
            else:
                display_items.append({'type': 'image', 'file': f})

        return template('''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Media Launcher</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
  <button id="menu-button">☰</button>
  <h1>Media Launcher</h1>
</header>
<main class="grid">
% for item in display_items:
  <a href="/media/{{item['file']}}" target="_blank" class="media-item">
    % if item['type'] == 'video':
      <img src="/thumbnails/{{item['thumb']}}" alt="{{item['file']}}">
    % else:
      <img src="/media/{{item['file']}}" alt="{{item['file']}}">
    % end
  </a>
% end
</main>
</body>
</html>
        ''', display_items=display_items)

    return app

if __name__ == '__main__':
    args = parse_args()
    app = create_app(args.media_folder, args.thumb_folder)
    run(app, host=args.host, port=args.port, debug=True)
