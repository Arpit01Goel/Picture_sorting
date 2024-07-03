import os
import shutil
from datetime import datetime
from pathlib import Path

def create_directory_structure(base_path):
    """
    Create a directory structure based on the year, month, and date of the picture files.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def get_unique_filename(target_dir, filename):
    """
    Generate a unique filename to avoid overwriting in the target directory.
    If the filename already exists, append a number to make it unique.
    """
    base_name, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(target_dir, unique_filename)):
        unique_filename = f"{base_name}_{counter}{extension}"
        counter += 1
    return unique_filename

def copy_picture(file_path, target_base_path):
    """
    Copy the picture to the target directory based on its creation date.
    Ensure that files are not overwritten by generating a unique filename if necessary.
    """
    # Get the creation time of the file
    creation_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    year = creation_time.strftime('%Y')
    month = creation_time.strftime('%m')
    day = creation_time.strftime('%d')

    # Create the target directory path
    target_dir = os.path.join(target_base_path, year, month, day)
    create_directory_structure(target_dir)

    # Generate a unique filename to avoid overwriting
    unique_filename = get_unique_filename(target_dir, os.path.basename(file_path))

    # Copy the file with the unique filename
    shutil.copy2(file_path, os.path.join(target_dir, unique_filename))

def search_and_arrange_pictures_and_videos(source_path, target_base_path):
    """
    Search for pictures and videos in the source directory and arrange them in the target directory
    based on the year, month, and date they were created. Print unique extensions of unsupported files.
    Now supports .cr2, .webp, and .heic files.
    """
    # Supported picture and video extensions, now including .cr2, .webp, and .heic
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mov', '.wmv', '.cr2', '.webp', '.heic')
    printed_extensions = set()

    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith(supported_extensions):
                file_path = os.path.join(root, file)
                copy_picture(file_path, target_base_path)
            else:
                # Check and print the unique extension of unsupported files
                extension = os.path.splitext(file)[1].lower()
                if extension not in printed_extensions:
                    print(f"Unsupported file extension found: {extension}")
                    printed_extensions.add(extension)

if __name__ == "__main__":
    source_folder = input("Enter the source folder path: ")
    target_folder = input("Enter the target folder path for arranging pictures and videos: ")

    search_and_arrange_pictures_and_videos(source_folder, target_folder)
    print("Pictures and videos have been arranged.")