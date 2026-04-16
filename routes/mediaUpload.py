from bottle import Bottle, request, template
import os
from services.thumbnails import generate_thumbnails
from services.streams import generate_streams
from pathlib import Path
import tempfile
import subprocess

def setup_mediaUpload(app, media_folder, thumb_folder):

    os.makedirs(media_folder, exist_ok=True)

    @app.route('/mediaUpload')
    def media_upload():
        return template('mediaUpload.html')

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
        if mime not in {'video/mp4', 'video/webm', 'image/gif', 'image/jpeg', 'image/png', 'image/heic', 'image/heif'}:
            return "File type not allowed (MIME)"

        save_path = os.path.join(media_folder, filename)

        if ext in {'.mp4', '.webm', '.gif'}:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp_path = tmp.name
            upload.save(tmp_path, overwrite=True)

            try:
                compress_media(tmp_path, save_path, ext, mime)
            finally:
                os.remove(tmp_path)

            generate_thumbnails(media_folder, thumb_folder)
            generate_streams(Path(save_path))
        else:
            upload.save(save_path, overwrite=True)

        return f"Uploaded {filename}"

def compress_media(tmp_path: str, save_path: str, ext: str, mime: str):
    TARGET_SIZE = 192
    command = [
        "ffmpeg", "-y",
        "-i", tmp_path,
        "-vf", f"scale='if(gt(iw,{TARGET_SIZE}),{TARGET_SIZE},-2)':'if(gt(ih,{TARGET_SIZE}),{TARGET_SIZE},-2)'",
        save_path
    ]
    subprocess.run(command, check=True)