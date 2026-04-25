import json
import subprocess
from pathlib import Path
import threading
import queue
from services.configs import load_config

# Global job queue
job_queue = queue.Queue()
processing = False

MEDIA_EXTENSIONS = {".webm", ".mp4", ".gif", ".jpeg", ".png"}

def start_background_processor():
    """Start the background worker thread once at startup"""
    global processing
    if not processing:
        processing = True
        thread = threading.Thread(target=_process_jobs, daemon=True)
        thread.start()

def _process_jobs():
    """Worker loop: processes one job at a time"""
    while True:
        media_path = job_queue.get()
        try:
            _generate_streams_worker(media_path)
            print(f"✓ Finished processing {media_path.name}")
        except Exception as e:
            print(f"✗ Error processing {media_path.name}: {e}")
        finally:
            job_queue.task_done()

def generate_streams(media_path: Path):
    """Queue the job (returns immediately)"""
    print(f"Queued: {media_path.name}")
    job_queue.put(media_path)

def _generate_streams_worker(media_path: Path):
    config = load_config()
    stream_folder = Path(config["stream_folder"])
    rotation = config.get("rotation", 0)

    for brightness in range(10, 110, 10):
        stream_name = f"{media_path.stem}.stream"
        output_path = stream_folder / str(brightness) / stream_name

        output_path.parent.mkdir(parents=True, exist_ok=True)

        command = [
            "sudo",
            "/home/hoolacane/hoolacane-rpi-led-matrix/utils/video-viewer",
            "--led-chain=3",
            "--led-parallel=3",
            "--led-slowdown-gpio=2",
            "--led-multiplexing=1",
            "-T4",
            "--led-pwm-bits=8",
            f"--led-brightness={brightness}",
            str(media_path),
            "-O",
            str(output_path),
            f"--led-pixel-mapper=Rotate:{rotation}",
        ]

        print(f"Generating stream for: {media_path.name} at brightness {brightness}")
        subprocess.run(command, check=True)

def get_missing_media(config) -> list[Path]:
    media_folder = Path(config["media_folder"])
    stream_folder = Path(config["stream_folder"])

    media_files = {
        file.stem: file
        for file in media_folder.iterdir()
        if file.is_file() and file.suffix.lower() in MEDIA_EXTENSIONS
    }

    missing = []
    for stem, media_path in sorted(media_files.items()):
        stream_name = f"{stem}.stream"
        # A file is fully compiled only if ALL brightness levels exist
        all_exist = all(
            (stream_folder / str(brightness) / stream_name).exists()
            for brightness in range(10, 110, 10)
        )
        if not all_exist:
            missing.append(media_path)

    return missing

if __name__ == "__main__":
    config = load_config()
    missing_files = get_missing_media(config)

    if not missing_files:
        print("All media files have been compiled.")
    else:
        print(f"Found {len(missing_files)} media file(s) to compile:")
        for path in missing_files:
            print(f"  - {path.name}")
            generate_streams(path)