import os
import sys
from textnode import TextNode, textType
from file_utils import copy_directory_recursive
from page_generator import generate_pages_recursive


def main():
    # Get base path from command line argument, default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Determine output directory based on whether this is a production build
    if base_path != "/":
        # Production build - use docs directory
        output_dir = "docs"
    else:
        # Development build - use public directory
        output_dir = "public"
    
    # Copy static files to output directory
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    dest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), output_dir)
    
    print(f"Copying static files from {static_path} to {dest_path}")
    copy_directory_recursive(static_path, dest_path)
    print("Static files copied successfully!")
    
    # Generate HTML pages recursively
    content_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template.html")
    
    generate_pages_recursive(content_path, template_path, dest_path, base_path)
    print("Pages generated successfully!")


if __name__ == "__main__":
    main()