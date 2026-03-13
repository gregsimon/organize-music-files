# Organize Music Files

A Python script to automatically organize your FLAC and MP3 audio files into a structured `<artist>/<album>/` directory hierarchy based on their metadata tags.

## Prerequisites

- Python 3.x
- `mutagen` library for reading audio metadata

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

Run the script by providing the path to the folder containing your audio files:

```bash
python organize-music-files.py <source_folder>
```

### Options

- `--dry-run`: Prints the actions that would be taken (folder creation and file moving) without actually moving any files on the disk. This is useful for verifying the behavior before committing to the changes.

```bash
python organize-music-files.py /path/to/my/music --dry-run
```

## Details

1. The script reads the `artist` and `album` tags from each FLAC and MP3 file.
2. It sanitizes the tags for safe file paths, replacing characters like `&` with `and`.
3. It moves the processed audio files to a new directory structure. **Note:** Currently, the destination directory is hardcoded to `/tmp/music-folders/<artist>/<album>/`.

If a file is missing metadata, the script uses fallbacks like "Unknown Artist" or "Unknown Album".
