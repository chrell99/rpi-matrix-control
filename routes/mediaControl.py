import os
from bottle import template, request
from services.rpi_led_matrix import start_videoviewer

def setup_mediaControl(app, media_folder, thumb_folder, streams_folder):
    @app.route('/mediaControl')
    def mediaControl():
        media_files = sorted([
            f for f in os.listdir(media_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))
        ])

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

        try:
            start_videoviewer(filename)
            return f"Started {filename}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.post("/delete")
    def do_delete():
        try:
            data = request.json
            files = data.get('files', [])
            
            if not files:
                return {"status": "error", "message": "No files provided"}, 400
            
            deleted = []
            errors = []
            
            for filename in files:
                if '..' in filename or filename.startswith('/'):
                    errors.append(f"Invalid filename: {filename}")
                    continue
                
                media_path = os.path.join(media_folder, filename)
                
                if not os.path.exists(media_path):
                    errors.append(f"File not found: {filename}")
                    continue
                
                try:
                    base_name = os.path.splitext(filename)[0]

                    os.remove(media_path)

                    thumb_path = os.path.join(thumb_folder, f"{base_name}.png")
                    if os.path.exists(thumb_path):
                        os.remove(thumb_path)

                    for brightness in range(10, 101, 10):
                        stream_brightness_folder = os.path.join(streams_folder, str(brightness))
                        stream_path = os.path.join(stream_brightness_folder, f"{base_name}.stream")
                        if os.path.exists(stream_path):
                            os.remove(stream_path)
                    
                    deleted.append(filename)
                except OSError as e:
                    errors.append(f"Error deleting {filename}: {str(e)}")
            
            return {
                "status": "success",
                "deleted": deleted,
                "errors": errors,
                "deleted_count": len(deleted),
                "error_count": len(errors)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500
