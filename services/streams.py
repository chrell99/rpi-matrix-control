import json
import subprocess
from pathlib import Path

MEDIA_EXTENSIONS = {".webm", ".mp4", ".gif", ".jpeg", ".png"}

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def main():
    config = load_config()

    media_folder = Path(config["media_folder"])
    stream_folder = Path(config["stream_folder"])
    rotation = config.get("rotation", 0)

    # Collect media files
    media_files = {
        file.stem: file
        for file in media_folder.iterdir()
        if file.is_file() and file.suffix.lower() in MEDIA_EXTENSIONS
    }

    # Collect existing .stream files
    stream_files = {
        file.stem
        for file in stream_folder.iterdir()
        if file.is_file() and file.suffix == ".stream"
    }

    for filename, media_path in sorted(media_files.items()):
        stream_name = f"{filename}.stream"

        if filename in stream_files:
            continue

        command = [
            "sudo",
            "/home/hoolacane/hoolacane-rpi-led-matrix/utils/video-viewer",
            "--led-chain=3",
            "--led-parallel=3",
            "--led-slowdown-gpio=2",
            "--led-multiplexing=1",
            "-T4",
            "--led-pwm-bits=8",
            str(media_path),
            "-O",
            str(stream_folder / stream_name),
            f'--led-pixel-mapper=Rotate:{rotation}'
        ]

        print(f"Generating stream for: {filename}")
        subprocess.run(command, check=True)

if __name__ == "__main__":
    main()
