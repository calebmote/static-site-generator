import os
from textnode import TextNode, textType
from file_utils import copy_directory_recursive
from page_generator import generate_page


def main():
    # Copy static files to public directory
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    public_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
    
    print(f"Copying static files from {static_path} to {public_path}")
    copy_directory_recursive(static_path, public_path)
    print("Static files copied successfully!")
    
    # Generate HTML page
    content_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "index.md")
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template.html")
    dest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "index.html")
    
    generate_page(content_path, template_path, dest_path)
    print("Page generated successfully!")


if __name__ == "__main__":
    main()