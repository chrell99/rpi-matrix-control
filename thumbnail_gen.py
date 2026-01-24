import os, subprocess

MEDIA_FOLDER = "hoolacane_media"
THUMB_FOLDER = "thumbnails"
os.makedirs(THUMB_FOLDER, exist_ok=True)

for f in os.listdir(MEDIA_FOLDER):
    if f.lower().endswith(('.mp4', '.webm')):
        base = os.path.splitext(f)[0]
        thumb_path = os.path.join(THUMB_FOLDER, base + ".png")
        if not os.path.exists(thumb_path):
            subprocess.run([
                "ffmpeg", "-y", "-i", os.path.join(MEDIA_FOLDER, f),
                "-vframes", "1", "-vf", "scale=300:-1", thumb_path
            ])
            print(f"Generated thumbnail for {f}")

