import os
from textnode import TextNode, textType
from file_utils import copy_directory_recursive
from page_generator import generate_pages_recursive


def main():
    # Copy static files to public directory
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    public_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
    
    print(f"Copying static files from {static_path} to {public_path}")
    copy_directory_recursive(static_path, public_path)
    print("Static files copied successfully!")
    
    # Generate HTML pages recursively
    content_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template.html")
    
    generate_pages_recursive(content_path, template_path, public_path)
    print("Pages generated successfully!")


if __name__ == "__main__":
    main()