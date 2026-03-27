import os
from text_operations import extract_title
from markdown_html import markdown_to_html_node
from pathlib import Path


def generate_page(from_path, template_path, dest_path, base_path="/"):
    """
    Generates an HTML page from markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Replace relative links with base path
    final_html = final_html.replace('href="/', f'href="{base_path}')
    final_html = final_html.replace('src="/', f'src="{base_path}')
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write HTML file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    """
    Recursively generates HTML pages from all markdown files in content directory.
    """
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    
    content_path = Path(dir_path_content)
    template_path = Path(template_path)
    dest_path = Path(dest_dir_path)
    
    # Find all markdown files in content directory
    for md_file in content_path.rglob("**/*.md"):
        # Calculate relative path from content directory
        rel_path = md_file.relative_to(content_path)
        
        # Calculate destination path maintaining same structure
        dest_file = dest_path / rel_path.with_suffix('.html')
        
        # Generate page
        generate_page(str(md_file), str(template_path), str(dest_file), base_path)
