import os
import subprocess
import argparse

VIDEO_EXTS = ('.mp4', '.webm')
THUMB_EXT = '.png'

def index_thumbnails(thumb_folder):
    """
    Return a set of thumbnail basenames (without extension).
    """
    if not os.path.exists(thumb_folder):
        return set()

    return {
        os.path.splitext(f)[0]
        for f in os.listdir(thumb_folder)
        if f.lower().endswith(THUMB_EXT)
    }

def generate_thumbnails(media_folder, thumb_folder, scale_width=300, quiet=True):
    os.makedirs(thumb_folder, exist_ok=True)

    media_files = [
        f for f in os.listdir(media_folder)
        if f.lower().endswith(VIDEO_EXTS)
    ]

    if not media_files:
        print("No video files found.")
        return

    existing_thumbs = index_thumbnails(thumb_folder)

    # Determine which media files actually need thumbnails
    to_generate = [
        f for f in media_files
        if os.path.splitext(f)[0] not in existing_thumbs
    ]

    if not to_generate:
        print("All thumbnails are up to date.")
        return

    print(f"Generating {len(to_generate)} thumbnail(s)...")

    for i, f in enumerate(to_generate, start=1):
        base = os.path.splitext(f)[0]
        thumb_path = os.path.join(thumb_folder, base + THUMB_EXT)

        cmd = [
            "ffmpeg", "-y",
            "-i", os.path.join(media_folder, f),
            "-vframes", "1",
            "-vf", f"scale={scale_width}:-1",
            thumb_path
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None
        )

        print(f"[{i}/{len(to_generate)}] {f}")

    print("Thumbnail generation complete.")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate missing thumbnails for video files"
    )
    parser.add_argument(
        '--media-folder',
        default=os.path.expanduser("~/media"),
        help='Media folder (default: ~/media)'
    )
    parser.add_argument(
        '--thumb-folder',
        default=os.path.expanduser("~/thumbnails"),
        help='Thumbnail folder (default: ~/thumbnails)'
    )
    parser.add_argument(
        '--scale-width',
        type=int,
        default=300,
        help='Thumbnail width (default: 300)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show ffmpeg output'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    generate_thumbnails(
        args.media_folder,
        args.thumb_folder,
        scale_width=args.scale_width,
        quiet=not args.verbose
    )