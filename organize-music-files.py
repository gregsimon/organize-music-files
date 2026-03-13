# Copyright 2025 Greg Simon.

import os
import shutil
import argparse
from mutagen.flac import FLAC

def organize_flac_files(source_folder, dry_run=False):
    """
    Organizes FLAC files from a source folder into a directory structure
    of <artist>/<album>/<song>.

    Args:
        source_folder (str): The path to the folder containing the FLAC files.
        dry_run (bool): If True, only prints out the steps instead of acting.
    """
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.flac'):
            source_path = os.path.join(source_folder, filename)

            try:
                audio = FLAC(source_path)

                # --- Get metadata, with fallbacks for missing tags ---
                artist = audio.get('artist', ['Unknown Artist'])[0]
                album = audio.get('album', ['Unknown Album'])[0]

                # replace ampersand with "and" in artist and album
                artist = artist.replace('&', 'and')
                album = album.replace('&', 'and')
                
                # --- Sanitize for file path safety ---
                safe_artist = "".join(c for c in artist if c.isalnum() or c in (' ', '.', '_')).rstrip()
                safe_album = "".join(c for c in album if c.isalnum() or c in (' ', '.', '_')).rstrip()


                # --- Create new directory structure and move the file ---
                destination_dir = os.path.join(source_folder, safe_artist, safe_album)
                
                # Currently overriding to /tmp/music-folders
                destination_dir = os.path.join("/tmp/music-folders/", safe_artist, safe_album)

                destination_path = os.path.join(destination_dir, filename)

                if dry_run:
                    print(f"[DRY RUN] Would create folder: {destination_dir}")
                    print(f"[DRY RUN] Would move file: {source_path} -> {destination_path}")
                else:
                    os.makedirs(destination_dir, exist_ok=True)
                    shutil.move(source_path, destination_path)
                    print(f"Moved: {filename} -> {destination_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Organizes FLAC files from a source folder into a directory structure of <artist>/<album>/<song>.")
    parser.add_argument('source_folder', help="The path to the folder containing the FLAC files.")
    parser.add_argument('--dry-run', action='store_true', help="Print the actions that would be taken without actually organizing the files.")
    
    args = parser.parse_args()
    
    organize_flac_files(args.source_folder, dry_run=args.dry_run)