"""
File Organizer

A Python script for automatically organizing files in the current directory
based on their extension, size, or by removing duplicate files.

Features:
- Organize files by extension (creates folders for each file type)
- Organize files by size (light, medium, heavy categories)
- Remove duplicate files while keeping one copy
- Comprehensive logging of all operations
- Error handling for file operations

Usage:
    python file_organizer.py [--extension | --size | --erase_duplicates]

Options:
    -e, --extension         Organize files by their extension
    -s, --size              Organize files by their size
    -d, --erase_duplicates  Remove duplicate files

Examples:
    python file_organizer.py --extension
    python file_organizer.py --size
    python file_organizer.py --erase_duplicates

Note: Only one option can be used at a time.

Dependencies:
    Requires only Python standard libraries:
    - os
    - shutil
    - glob
    - argparse
    - logging
    - filecmp

Author: Hossein Naseri
License: MIT
Version: 1.0
"""
import os
import shutil
import glob
import argparse
import logging
from filecmp import cmp


# Global variable's (files -> [all files in the current folder])
#                   (extension_set -> set(all extension that exists in files)
files = sorted(list(filter(lambda x: "." in x, glob.glob("*"))))
extensions_set = set()
files_size = {}
current_file = __file__.split("/")[-1]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add all extension's in file's to extension_set
for file in files:
    name, extension = os.path.splitext(file)
    extensions_set.add(extension[1:])
    stat_res = os.stat(file)
    files_size[file] = round((stat_res.st_size / 1024) / 1024, 2)


files_size = dict(sorted(files_size.items(), key=lambda item: item[1],
                         reverse=True))


size = list(files_size.values())[0]
def create_folders(in_order = "extension"):
    """Create Folders for each extension in extensions_set in current directory.
    """
    if in_order == "extension":
        for ext in extensions_set:
            os.makedirs(f"{ext}_files", exist_ok=True)
    if in_order == "size":
        os.makedirs("light_files", exist_ok=True)
        os.makedirs("medium_files", exist_ok=True)
        os.makedirs("heavy_files", exist_ok=True)


def erase_empty_folders():
    """Erase all empty files in current directory."""
    folders =  ["light_files", "medium_files", "heavy_files"]
    for folder in folders:
        check = os.listdir(folder)
        if len(check) == 0:
            os.rmdir(folder)


def move_files(in_order="extension"):
    """Move all files in current_folder to ext_files directories."""

    if in_order not in ["extension", "size", "creation_date",
                        "erase_duplicates"]:
        in_order = "extension"

    if in_order == "extension":
        for file in files:
            name, ext = os.path.splitext(file)
            path = f"{ext[1:]}_files/{name}{ext}"
            if file != current_file and not os.path.exists(path):
                try:
                    shutil.move(file, path)
                    logging.info(f"Moving {file} to {path}")
                except Exception as e:
                    logging.error(f"Failed to move {file} to {path}: {str(e)}")
            elif file != current_file:
                logging.warning(
                    f"Destination {path} already exists, skipping {file}")

    if in_order == "size":
        for key, value in files_size.items():
            if key == current_file:
                continue

            if value < 500:
                try:
                    shutil.move(f"{key}", f"light_files/{key}")
                    logging.info(f"Moving {key} to {value}")
                except Exception as e:
                    logging.error(f"Failed to move {key} to {value}: {str(e)}")

            elif value in range(500, 1024):
                try:
                    shutil.move(f"{key}", f"medium_files/{key}")
                    logging.info(f"Moving {key} to {value}")
                except Exception as e:
                    logging.error(f"Failed to move {key} to {value}: {str(e)}")

            elif value > 1024:
                try:
                    shutil.move(f"{key}", f"heavy_files/{key}")
                    logging.info(f"Moving {key} to {value}")
                except Exception as e:
                    logging.error(f"Failed to move {key} to {value}: {str(e)}")

        erase_empty_folders()

    if in_order == "erase_duplicates":
        duplicates = []
        for file in files:
            if_dup = False

            for class_ in duplicates:
                if_dup = cmp(file, class_[0], shallow=False)

                if if_dup:
                    class_.append(file)
                    break

            if not if_dup:
                duplicates.append([file])

        for item in sorted(duplicates, reverse=True):
            if len(item) > 1:
                for i in range(len(item) - 1):
                    os.remove(item[i])
                    logger.info(f"Removing {item[i]}")


def main(extension=False, size=False, erase_duplicates=False):
    """Main function for organizing all files in current directory by extension.
    """
    if extension:
        create_folders("extension")
        move_files("extension")

    elif size:
        create_folders("size")
        move_files("size")

    elif erase_duplicates:
        move_files("erase_duplicates")

    else:
        print("Only one can be True at the time.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Organizer Py")

    parser.add_argument(
        "-e", "--extension", action="store_true",
        help="Organize all files in current directory in order of extension."
    )
    parser.add_argument(
        "-s", "--size", action="store_true",
        help="Organize all files in current directory in order of size."
    )
    parser.add_argument(
        "-d", "--erase_duplicates", action="store_true",
        help="Erase duplicate files in current directory."
    )
    args = parser.parse_args()


    # Main function
    main(
        extension = args.extension,
        size = args.size,
        erase_duplicates = args.erase_duplicates
    )
