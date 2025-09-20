"""
File Organizer

A Python script for automatically organizing files in a specified directory
based on their extension, size, last modification date, or by removing duplicate files.

Features:
- Organize files by extension (creates folders for each file type)
- Organize files by size (light, medium, heavy categories)
- Organize files by last modification date (using Persian calendar when available)
- Remove duplicate files while keeping one copy
- Comprehensive logging of all operations with both file and console output
- Error handling for file operations with detailed error messages
- Cross-platform compatibility with proper path handling

Usage:
    python file_organizer.py [--extension | --size | --last_modify_date | --erase_duplicates] [--path PATH]

Options:
    -e, --extension         Organize files by their extension
    -s, --size              Organize files by their size
    -l, --last_modify_date  Organize files by last modification date
    -d, --erase_duplicates  Remove duplicate files
    -p, --path PATH         Path to the directory to organize (optional)

Examples:
    python file_organizer.py --extension
    python file_organizer.py --size --path /path/to/directory
    python file_organizer.py --last_modify_date
    python file_organizer.py --erase_duplicates

Note: Only one option can be used at a time.

Dependencies:
    Standard Python libraries with optional khayyam support:
    - os, shutil, glob, argparse, logging, filecmp, hashlib, datetime
    - khayyam (optional, for Persian date functionality)

Author: Hossein Naseri
License: MIT
Version: 2.0
"""

import os
import shutil
import glob
import argparse
import logging
import hashlib
from datetime import datetime
from filecmp import cmp

try:
    from khayyam import JalaliDatetime
    KHAYYAM_AVAILABLE = True
except ImportError:
    KHAYYAM_AVAILABLE = False
    logging.warning("khayyam library not found. Using Gregorian calendar instead.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("file_organizer.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_files(path="."):
    """
    Retrieve all files in the specified directory.

    Args:
        path (str): Path to the directory to scan for files

    Returns:
        list: Sorted list of file paths in the directory
    """
    try:
        all_items = glob.glob(os.path.join(path, "*"))
        files = [
            item for item in all_items
            if os.path.isfile(item) and os.path.basename(item) not in [os.path.basename(__file__), "file_organizer.log"]
        ]
        return sorted(files)
    except Exception as e:
        logger.error(f"Error retrieving files: {e}")
        return []

def get_file_size(file_path):
    """
    Get file size in megabytes.

    Args:
        file_path (str): Path to the file

    Returns:
        float: File size in MB rounded to 2 decimal places
    """
    try:
        stat_res = os.stat(file_path)
        return round(stat_res.st_size / (1024 * 1024), 2)
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return 0

def calculate_file_hash(file_path, chunk_size=8192):
    """
    Calculate MD5 hash of a file for duplicate detection.

    Args:
        file_path (str): Path to the file
        chunk_size (int): Size of chunks to read at a time

    Returns:
        str: MD5 hash of the file content or None on error
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating hash for {file_path}: {e}")
        return None

def create_folders(path, folder_names):
    """
    Create necessary folders for organization.

    Args:
        path (str): Base path where folders should be created
        folder_names (list): List of folder names to create
    """
    for folder_name in folder_names:
        folder_path = os.path.join(path, folder_name)
        try:
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Created folder: {folder_path}")
        except Exception as e:
            logger.error(f"Error creating folder {folder_path}: {e}")

def erase_empty_folders(path, folder_names):
    """
    Remove empty folders from the directory.

    Args:
        path (str): Base path where folders are located
        folder_names (list): List of folder names to check and remove if empty
    """
    for folder_name in folder_names:
        folder_path = os.path.join(path, folder_name)
        try:
            if (os.path.exists(folder_path) and
                os.path.isdir(folder_path) and
                not os.listdir(folder_path)):
                os.rmdir(folder_path)
                logger.info(f"Removed empty folder: {folder_path}")
        except Exception as e:
            logger.error(f"Error removing folder {folder_path}: {e}")

def organize_by_extension(files, path):
    """
    Organize files based on their extensions.

    Args:
        files (list): List of file paths to organize
        path (str): Base path where files are located
    """
    extensions_set = set()
    for file_path in files:
        _, ext = os.path.splitext(file_path)
        if ext:
            extensions_set.add(ext[1:].lower())

    # Create folders for each extension
    folder_names = [f"{ext}_files" for ext in extensions_set]
    create_folders(path, folder_names)

    # Move files to their respective folders
    for file_path in files:
        try:
            file_name = os.path.basename(file_path)
            _, ext = os.path.splitext(file_name)
            if ext:
                ext = ext[1:].lower()
                dest_folder = os.path.join(path, f"{ext}_files")
                dest_path = os.path.join(dest_folder, file_name)
                shutil.move(file_path, dest_path)
                logger.info(f"Moved file: {file_name} → {dest_folder}/")
        except Exception as e:
            logger.error(f"Error moving file {file_name}: {e}")

def organize_by_size(files, path):
    """
    Organize files based on their size.

    Args:
        files (list): List of file paths to organize
        path (str): Base path where files are located
    """
    # Create folders for size categories
    folder_names = ["light_files", "medium_files", "heavy_files"]
    create_folders(path, folder_names)

    # Move files to appropriate folders based on size
    for file_path in files:
        try:
            file_name = os.path.basename(file_path)
            size_mb = get_file_size(file_path)

            if size_mb < 10:  # Light: less than 10MB
                dest_folder = "light_files"
            elif size_mb < 100:  # Medium: less than 100MB
                dest_folder = "medium_files"
            else:  # Heavy: more than 100MB
                dest_folder = "heavy_files"

            dest_path = os.path.join(path, dest_folder, file_name)
            shutil.move(file_path, dest_path)
            logger.info(f"Moved file: {file_name} → {dest_folder}/ (size: {size_mb} MB)")
        except Exception as e:
            logger.error(f"Error moving file {file_name}: {e}")

    # Remove empty size folders
    erase_empty_folders(path, folder_names)

def organize_by_last_modify_date(files, path):
    """
    Organize files based on their last modification date.

    Args:
        files (list): List of file paths to organize
        path (str): Base path where files are located
    """
    folder_names = set()

    # First, collect all unique folder names
    for file_path in files:
        try:
            modify_time = os.path.getmtime(file_path)
            if KHAYYAM_AVAILABLE:
                folder_name = str(JalaliDatetime.fromtimestamp(modify_time).strftime('%Y-%m-%d'))
            else:
                folder_name = datetime.fromtimestamp(modify_time).strftime('%Y-%m-%d')
            folder_names.add(folder_name)
        except Exception as e:
            logger.error(f"Error getting modification time for {file_path}: {e}")

    # Create all folders
    create_folders(path, list(folder_names))

    # Move files to appropriate folders
    for file_path in files:
        try:
            file_name = os.path.basename(file_path)
            modify_time = os.path.getmtime(file_path)

            if KHAYYAM_AVAILABLE:
                folder_name = str(JalaliDatetime.fromtimestamp(modify_time).strftime('%Y-%m-%d'))
            else:
                folder_name = datetime.fromtimestamp(modify_time).strftime('%Y-%m-%d')

            dest_folder = os.path.join(path, folder_name)
            dest_path = os.path.join(dest_folder, file_name)
            shutil.move(file_path, dest_path)
            logger.info(f"Moved file: {file_name} → {dest_folder}/")
        except Exception as e:
            logger.error(f"Error moving file {file_name}: {e}")

def remove_duplicates(files, path):
    """
    Remove duplicate files while keeping one copy of each.

    Args:
        files (list): List of file paths to check for duplicates
        path (str): Base path where files are located
    """
    # Group files by size first for efficiency
    files_by_size = {}
    for file_path in files:
        try:
            size = os.path.getsize(file_path)
            if size not in files_by_size:
                files_by_size[size] = []
            files_by_size[size].append(file_path)
        except Exception as e:
            logger.error(f"Error getting size for {file_path}: {e}")

    # Find and remove duplicates
    duplicates = []
    for size, file_list in files_by_size.items():
        if len(file_list) > 1:
            # Use hashing for more accurate duplicate detection
            file_hashes = {}
            for file_path in file_list:
                file_hash = calculate_file_hash(file_path)
                if file_hash:
                    if file_hash in file_hashes:
                        duplicates.append(file_path)
                    else:
                        file_hashes[file_hash] = file_path

    # Remove duplicate files
    for dup_file in duplicates:
        try:
            os.remove(dup_file)
            logger.info(f"Removed duplicate: {os.path.basename(dup_file)}")
        except Exception as e:
            logger.error(f"Error removing duplicate {dup_file}: {e}")

def main():
    """Main function to handle command line arguments and execute organization tasks."""
    parser = argparse.ArgumentParser(description="File Organizer Py")
    parser.add_argument(
        "-e", "--extension", action="store_true",
        help="Organize files by their extension"
    )
    parser.add_argument(
        "-s", "--size", action="store_true",
        help="Organize files by their size"
    )
    parser.add_argument(
        "-l", "--last_modify_date", action="store_true",
        help="Organize files by last modification date"
    )
    parser.add_argument(
        "-d", "--erase_duplicates", action="store_true",
        help="Remove duplicate files"
    )
    parser.add_argument(
        "-p", "--path", type=str, default=".",
        help="Path to directory (default: current directory)"
    )

    args = parser.parse_args()

    # Check if only one option is selected
    options = [args.extension, args.size, args.erase_duplicates, args.last_modify_date]
    if sum(options) != 1:
        logger.error(
            "Please specify exactly one option: --extension, --size, --last_modify_date, or --erase_duplicates"
        )
        return

    path = os.path.abspath(args.path)
    if not os.path.exists(path):
        logger.error(f"The path {path} does not exist.")
        return

    if not os.path.isdir(path):
        logger.error(f"The path {path} is not a directory.")
        return

    files = get_files(path)
    if not files:
        logger.warning("No files found to organize.")
        return

    logger.info(f"Found {len(files)} files to organize in {path}")

    if args.extension:
        organize_by_extension(files, path)
    elif args.size:
        organize_by_size(files, path)
    elif args.last_modify_date:
        organize_by_last_modify_date(files, path)
    elif args.erase_duplicates:
        remove_duplicates(files, path)

    logger.info("Organization completed!")

if __name__ == "__main__":
    main()