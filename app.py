from bottle import Bottle, static_file, template, run
import os

# Folders
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), "hoolacane_media")
THUMB_FOLDER = os.path.join(os.path.dirname(__file__), "thumbnails")

app = Bottle()

# Serve static files
@app.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static')

# Serve media files
@app.route('/media/<filename:path>')
def serve_media(filename):
    return static_file(filename, root=MEDIA_FOLDER)

# Serve thumbnails
@app.route('/thumbnails/<filename:path>')
def serve_thumb(filename):
    return static_file(filename, root=THUMB_FOLDER)

@app.route('/')
def index():
    media_files = os.listdir(MEDIA_FOLDER)
    media_files = [f for f in media_files if f.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))]

    display_items = []
    for f in media_files:
        if f.lower().endswith(('.mp4', '.webm')):
            # Use corresponding thumbnail if it exists
            base_name = os.path.splitext(f)[0]
            thumb_file = base_name + ".png"
            if not os.path.exists(os.path.join(THUMB_FOLDER, thumb_file)):
                # Optional: fallback to a placeholder
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

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)

