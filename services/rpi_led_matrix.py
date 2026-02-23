import json
import subprocess, os, signal
from pathlib import Path

_last_process = None

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def start_videoviewer(filename):
    global _last_process

    stop_running_process()

    config = load_config()
    stream_folder = Path(config["stream_folder"])
    media_folder = Path(config["media_folder"])
    rotation = config.get("rotation", 0)

    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        cmd = [
            "sudo",
            "/home/hoolacane/hoolacane-rpi-led-matrix/utils/led-image-viewer",
            "--led-chain=3",
            "--led-parallel=3",
            "--led-slowdown-gpio=2",
            "--led-multiplexing=1",
            f'--led-pixel-mapper=Rotate:{rotation}',
            str(media_folder / filename)
        ]
    else:
        stream_name = f"{os.path.splitext(filename)[0]}.stream"

        cmd = [
            "sudo",
            "/home/hoolacane/hoolacane-rpi-led-matrix/utils/led-image-viewer",
            "--led-chain=3",
            "--led-parallel=3",
            "--led-slowdown-gpio=2",
            "--led-multiplexing=1",
            str(stream_folder / stream_name),
        ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started process with PID {process.pid}")
    _last_process = process

def stop_running_process():
    global _last_process
    if _last_process is None:
        return

    # Terminate politely first
    if _last_process.poll() is None:  # still running
        _last_process.terminate()
        try:
            _last_process.wait(timeout=5)  # wait up to 5 seconds
        except subprocess.TimeoutExpired:
            _last_process.kill()           # force kill if needed
            _last_process.wait()           # reap it

    _last_process = None

def start_strobe(on_time, off_time, brightness):
    global _last_process

    stop_running_process()

    cmd = [
        "sudo",
        "/home/hoolacane/hoolacane-rpi-led-matrix/music-synced/strobe",
        str(on_time),
        str(off_time),
        str(brightness),
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started process with PID {process.pid}")
    _last_process = process

