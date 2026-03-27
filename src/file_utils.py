import os
import shutil


def copy_directory_recursive(source, destination):
    """
    Recursively copies all contents from source directory to destination directory.
    First deletes all contents of destination directory to ensure clean copy.
    Logs the path of each file copied.
    """
    # Delete destination directory if it exists
    if os.path.exists(destination):
        print(f"Deleting existing directory: {destination}")
        shutil.rmtree(destination)
    
    # Create destination directory
    print(f"Creating directory: {destination}")
    os.makedirs(destination)
    
    # Copy all contents from source to destination
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        
        if os.path.isfile(source_path):
            # Copy file
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            # Recursively copy directory
            copy_directory_recursive(source_path, destination_path)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages from markdown files.
    This is a placeholder for future implementation.
    """
    pass
