# Copyright 2025 Greg Simon.

import os
import shutil
import argparse
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def organize_audio_files(source_folder, destination_folder, dry_run=False):
    """
    Organizes FLAC and MP3 files from a source folder into a directory structure
    of <artist>/<album>/<song>.

    Args:
        source_folder (str): The path to the folder containing the audio files.
        dry_run (bool): If True, only prints out the steps instead of acting.
    """
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.flac', '.mp3')):
            source_path = os.path.join(source_folder, filename)

            try:
                if filename.lower().endswith('.flac'):
                    audio = FLAC(source_path)
                else:
                    audio = MP3(source_path, ID3=EasyID3)

                # --- Get metadata, with fallbacks for missing tags ---
                artist_tags = audio.get('artist', ['Unknown Artist'])
                artist = artist_tags[0] if artist_tags else 'Unknown Artist'
                
                album_tags = audio.get('album', ['Unknown Album'])
                album = album_tags[0] if album_tags else 'Unknown Album'

                # replace ampersand with "and" in artist and album
                artist = artist.replace('&', 'and')
                album = album.replace('&', 'and')
                
                # --- Sanitize for file path safety ---
                safe_artist = "".join(c for c in artist if c.isalnum() or c in (' ', '.', '_')).rstrip()
                safe_album = "".join(c for c in album if c.isalnum() or c in (' ', '.', '_')).rstrip()


                # --- Create new directory structure and move the file ---
                destination_dir = os.path.join(destination_folder, safe_artist, safe_album)

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
    parser = argparse.ArgumentParser(description="Organizes FLAC and MP3 files from a source folder into a directory structure of <artist>/<album>/<song>.")
    parser.add_argument('source_folder', help="The path to the folder containing the audio files.")
    parser.add_argument('destination_folder', help="The path to the destination folder where organized files will be placed.")
    parser.add_argument('--dry-run', action='store_true', help="Print the actions that would be taken without actually organizing the files.")
    
    args = parser.parse_args()
    
    organize_audio_files(args.source_folder, args.destination_folder, dry_run=args.dry_run)