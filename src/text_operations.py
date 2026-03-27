from textnode import TextNode, textType
import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    
    # Strip leading/trailing whitespace from each block
    stripped_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:  # Only add non-empty blocks
            stripped_blocks.append(stripped)
    
    return stripped_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    
    # Check for heading (1-6 # characters followed by space)
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by space)
    if all(re.match(r"^\-\s", line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. followed by space, starting at 1)
    ordered_pattern = re.compile(r"^(\d+)\.\s")
    if all(ordered_pattern.match(line) for line in lines):
        numbers = []
        for line in lines:
            match = ordered_pattern.match(line)
            if match:
                numbers.append(int(match.group(1)))
        
        # Check if numbers start at 1 and increment by 1
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip().lstrip('# ').strip()
    
    raise ValueError("No h1 header found in markdown")
