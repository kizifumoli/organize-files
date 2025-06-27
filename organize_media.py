from pathlib import Path
from typing import List, Any, Dict
import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta

def hash_file(path: Path) -> str:
    with open(path, "rb") as fd:
        digest = hashlib.file_digest(fd, "sha256")
    return str(digest.hexdigest())

def move_files(extensions: List[str], src_dir:Path, dest_dir: Path):
    file_json_path = dest_dir / "file_hashes.json"

    file_json = {
        "hashes": []
    }

    try:
        if file_json_path.exists():
            with open(file_json_path) as fd:
                file_json = json.load(fd)
                if "hashes" not in file_json:
                    file_json["hashes"] = []

    except json.decoder.JSONDecodeError as err:
        print(f"Warning... {file_json_path} unable to be read successfully ({err}). Continuing...")


    hash_set = set(file_json["hashes"])
    print("B")

    num_files_moved = 0
    for ext in extensions:
        files = src_dir.glob(f"*.{ext}")
        for f_path in files:
            file_hash = str(hash_file(f_path))
            if file_hash in hash_set:
                print(f"Collision at {file_hash}... Skipping")
                continue

            # Figure out when the file was modified and what week's directory to place it in.
            modified_time = datetime.fromtimestamp(f_path.stat().st_mtime)
            start_of_week = modified_time - timedelta(modified_time.weekday())

            week_str = start_of_week.strftime("%Y-%m-%d")
            hash_set.add(file_hash)
            
            # Rename 
            week_directory = dest_dir / week_str
            if not week_directory.exists():
                week_directory.mkdir(exist_ok=True, parents=True)

            dest_filepath = week_directory / f"{file_hash}.{ext}"
            f_path.rename(dest_filepath)
            num_files_moved += 1

    file_json = {
        "hashes": list(hash_set),
        "modified_at": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")        
    }

    with open(file_json_path, "w") as json_out_fd:
        json.dump(file_json, json_out_fd, indent="  ")

    print(f"Moved {num_files_moved} files")

def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir",
                        type=Path,
                        default=Path.home() / "Downloads",
                        help="directory where files will be moved from")
    parser.add_argument("-images-dir",
                        type=Path,
                        default=Path.home() / "Documents/Personal/Hobbies/Memes/",
                        help="directory where images will be moved to")
    parser.add_argument("--videos-dir",
                        type=Path,
                        default=Path.home() / "Videos/Memes",
                        help="directory where videos will be moved from")
    return parser

def main():
    if len(sys.argv) < 1:
        print("Too few arguments... Exiting")
        sys.exit(1)

    argparser = create_argparser()
    args = argparser.parse_args()

    image_extensions = ["jpg", "jpeg", "png", "webp", "gif"]
    video_extensions = ["mkv", "webm", "mp4"]

    move_files(image_extensions, args.source_dir, args.images_dir)
    move_files(video_extensions, args.source_dir, args.videos_dir)

if __name__ == "__main__":
    print("Ah!")
    main()
