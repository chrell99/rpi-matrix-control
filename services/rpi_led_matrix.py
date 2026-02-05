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

    stream_name = f"{filename}.stream"

    cmd = [
        "sudo",
        "/home/hoolacane/hoolacane-rpi-led-matrix/utils/led-image-viewer",
        "--led-chain=3",
        "--led-parallel=3",
        "--led-slowdown-gpio=2",
        "--led-multiplexing=1",
        str(stream_folder / stream_name),
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

    print(f"Started process with PID {process.pid}")
    _last_process = process.pid

def stop_running_process():
    global _last_process
    if _last_process is None:
        return
    
    os.kill(_last_process, signal.SIGKILL)
    _last_process = None




