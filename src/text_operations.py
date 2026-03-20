from textnode import TextNode, textType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != textType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        
        # Handle empty text case
        if text == "":
            new_nodes.append(old_node)
            continue
        
        sections = text.split(delimiter)
        
        # Handle case where text is only delimiters
        if len(sections) == 2 and sections[0] == "" and sections[1] == "":
            new_nodes.append(TextNode("", text_type))
            continue
        
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unclosed delimiter '{delimiter}'")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
                
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], textType.PLAIN))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    # Negative lookahead to avoid matching images (which start with !)
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != textType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(old_node)
            continue
        
        current_text = text
        for image_alt, image_url in images:
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], textType.PLAIN))
            new_nodes.append(TextNode(image_alt, textType.IMAGE, image_url))
            current_text = sections[1]
        
        if current_text:
            new_nodes.append(TextNode(current_text, textType.PLAIN))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != textType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(old_node)
            continue
        
        current_text = text
        for link_text, link_url in links:
            sections = current_text.split(f"[{link_text}]({link_url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], textType.PLAIN))
            new_nodes.append(TextNode(link_text, textType.LINK, link_url))
            current_text = sections[1]
        
        if current_text:
            new_nodes.append(TextNode(current_text, textType.PLAIN))
    
    return new_nodes


def text_to_textnodes(text):
    initial_node = TextNode(text, textType.PLAIN)
    nodes = [initial_node]
    
    # Process in order: images first, then links, then formatting
    # For formatting, process code first (most specific), then italic, then bold
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", textType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", textType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", textType.BOLD)
    
    return nodes
