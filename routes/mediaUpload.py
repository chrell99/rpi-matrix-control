from bottle import Bottle, request, template
import os
from services.thumbnails import generate_thumbnails
from services.streams import generate_streams
from pathlib import Path

def setup_mediaUpload(app, media_folder, thumb_folder):

    os.makedirs(media_folder, exist_ok=True)

    @app.route('/mediaUpload')
    def media_upload():
        existing_files = [
            f.lower() for f in os.listdir(media_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))
        ]
        return template('mediaUpload.html',  existing_files=existing_files)


    @app.post("/upload")
    def do_upload():
        upload = request.files.get('upload')

        if not upload:
            return "No file uploaded"

        filename = os.path.basename(upload.filename)
        ext = os.path.splitext(filename)[1].lower()
        mime = upload.content_type

        if ext not in {'.mp4', '.webm', '.gif', '.jpg', '.jpeg', '.png', '.heic'}:
            return "File type not allowed (extension)"

        if mime not in {'video/mp4','video/webm','image/gif','image/jpeg','image/png','image/heic','image/heif'}:
            return "File type not allowed (MIME)"
        
        save_path = os.path.join(media_folder, filename)

        upload.save(save_path, overwrite=True)

        if ext in {'.mp4', '.webm', '.gif'}:
            generate_thumbnails(media_folder, thumb_folder)
            generate_streams(Path(save_path))

        return f"Uploaded {filename}"