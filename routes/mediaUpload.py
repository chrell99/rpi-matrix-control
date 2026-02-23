from bottle import Bottle, request, run, template
import os

def setup_mediaUpload(app, media_folder):

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

        if mime not in {'video/mp4','video/webm','image/gif','image/jpeg','image/png','image/heic','image/heif'}:
            return "File type not allowed (MIME)"
        
        save_path = os.path.join(media_folder, filename)

        upload.save(save_path, overwrite=True)

        return f"Uploaded {filename}"