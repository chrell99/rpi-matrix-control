import os
import subprocess
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate thumbnails for video files in a media folder"
    )
    parser.add_argument(
        '--media-folder',
        default=os.path.expanduser("~/media"),
        help='Folder where media files are stored (default: ~/media)'
    )
    parser.add_argument(
        '--thumb-folder',
        default=os.path.expanduser("~/thumbnails"),
        help='Folder where thumbnails will be saved (default: ~/thumbnails)'
    )
    parser.add_argument(
        '--scale-width',
        type=int,
        default=300,
        help='Width to scale thumbnails to while keeping aspect ratio (default: 300)'
    )
    return parser.parse_args()

def generate_thumbnails(media_folder, thumb_folder, scale_width):
    os.makedirs(thumb_folder, exist_ok=True)
    media_files = [f for f in os.listdir(media_folder) if f.lower().endswith(('.mp4', '.webm'))]

    if not media_files:
        print("No video files found in", media_folder)
        return

    print(f"Generating thumbnails for {len(media_files)} video(s)...")
    for idx, f in enumerate(media_files, start=1):
        base = os.path.splitext(f)[0]
        thumb_path = os.path.join(thumb_folder, base + ".png")
        if os.path.exists(thumb_path):
            print(f"[{idx}/{len(media_files)}] Skipping {f} (already exists)")
            continue

        # Run ffmpeg to generate thumbnail
        subprocess.run([
            "ffmpeg", "-y", "-i", os.path.join(media_folder, f),
            "-vframes", "1", "-vf", f"scale={scale_width}:-1", thumb_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # suppress ffmpeg output
        print(f"[{idx}/{len(media_files)}] Generated thumbnail for {f}")

    print("Thumbnail generation complete.")

if __name__ == "__main__":
    args = parse_args()
    generate_thumbnails(args.media_folder, args.thumb_folder, args.scale_width)
