import json
import subprocess, os, signal
from pathlib import Path
from services.settings import get_setting
from services.configs import load_config

_last_process = None

def start_videoviewer(filename):
    global _last_process

    stop_running_process()

    config = load_config()
    stream_folder = Path(config["stream_folder"])
    media_folder = Path(config["media_folder"])
    rotation = config.get("rotation", 0)
    brightness = get_setting("brightness")

    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        cmd = [
            "sudo",
            "/home/hoolacane/hoolacane-rpi-led-matrix/utils/led-image-viewer",
            "--led-chain=3",
            "--led-parallel=3",
            "--led-slowdown-gpio=2",
            "--led-multiplexing=1",
            f'--led-brightness={brightness}',
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
            str(stream_folder / str(brightness) / stream_name),
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
        "/home/hoolacane/hoolacane-rpi-led-matrix/custom-utils/strobe",
        str(on_time),
        str(off_time),
        str(brightness),
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started process with PID {process.pid}")
    _last_process = process

def start_strobe_to_beat():
    global _last_process

    stop_running_process()

    brightness = get_setting("brightness")
    sensitivity = get_setting("strobe_to_beat_sensitivity")
    window = get_setting("strobe_to_beat_window")

    cmd = [
        "sudo",
        "/home/hoolacane/hoolacane-rpi-led-matrix/music-synced/strobe-to-freq",
        f'--brightness={brightness}',
        f'--sensitivity={sensitivity}',
        f'--window={window}'
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started process with PID {process.pid}")
    _last_process = process

def start_spectrum_visualizer():
    global _last_process

    stop_running_process()

    brightness = get_setting("brightness")
    freq_from = get_setting("spectrum_visualizer_freq_from")
    freq_to = get_setting("spectrum_visualizer_freq_to")
    dnr = get_setting("spectrum_visualizer_dnr")
    droprate = get_setting("spectrum_visualizer_droprate")
    rise_smoothness = get_setting("spectrum_visualizer_rise_smoothness")
    lerp = get_setting("spectrum_visualizer_lerp")
    window_length_seconds = get_setting("spectrum_visualizer_window_length_seconds")

    cmd = [
        "sudo",
        "/home/hoolacane/hoolacane-rpi-led-matrix/music-synced/spectrum-visualizer",
        f'{freq_from}',
        f'{freq_to}',
        f'{brightness}',
        f'{dnr}',
        f'{droprate}',
        f'{rise_smoothness}',
        f'{lerp}',
        f'{window_length_seconds}'
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started process with PID {process.pid}")
    _last_process = process

def start_name_picker():
    global _last_process

    stop_running_process()

    font_dir = Path("/home/hoolacane/hoolacane-rpi-led-matrix/fonts")

    brightness = get_setting("brightness")
    main_font = str(font_dir / get_setting("name_picker_main_font"))
    secondary_font = str(font_dir / get_setting("name_picker_secondary_font"))
    starting_speed = get_setting("name_picker_starting_speed")
    friction = get_setting("name_picker_friction")
    min_speed = get_setting("name_picker_minimum_speed")
    top_text = get_setting("name_picker_top_text")
    top_text_speed = get_setting("name_picker_top_text_speed")
    bottom_text = get_setting("name_picker_bottom_text")
    bottom_text_speed = get_setting("name_picker_bottom_text_speed")
    top_bottom_text_gap = get_setting("name_picker_top_bottom_text_gap")
    names_list = get_setting("name_picker_names")
    names_string = ",".join(names_list)

    cmd = [
        "sudo",
        "/home/hoolacane/hoolacane-rpi-led-matrix/custom-utils/name-picker",
        "-B", str(brightness),
        "-s", str(starting_speed),
        "-F", str(friction),
        "-m", str(min_speed),
        "-f", main_font,
        "-g", secondary_font,
        "-T", top_text,
        "-U", str(top_text_speed),
        "-L", bottom_text,
        "-V", str(bottom_text_speed),
        "-G", str(top_bottom_text_gap),
        "-i", names_string
    ]

    if get_setting("name_picker_celebration"):
        cmd.append("-e")

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started process with PID {process.pid}")
    _last_process = process

def start_roulette():
    global _last_process

    stop_running_process()

    font_dir = Path("/home/hoolacane/hoolacane-rpi-led-matrix")

    bdf_font = str(font_dir / get_setting("roulette_bdf_font_file"))
    winner_font = str(font_dir / get_setting("roulette_winner_font_file"))
    
    speed = get_setting("roulette_speed")
    ball_speed = get_setting("roulette_ball_speed")
    friction = get_setting("roulette_friction")
    min_speed = get_setting("roulette_min_speed")
    brightness = get_setting("brightness")

    cmd = [
        "sudo",
        "/home/hoolacane/hoolacane-rpi-led-matrix/custom-utils/roulette",
        "-f", bdf_font,
        "-w", winner_font,
        "-s", str(speed),
        "-b", str(ball_speed),
        "-F", str(friction),
        "-m", str(min_speed),
        "-B", str(brightness)
    ]

    if get_setting("roulette_do_fireworks"):
        cmd.append("-e")

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Started roulette process with PID {process.pid}")
    _last_process = process
