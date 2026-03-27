from textnode import TextNode, textType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_operations import markdown_to_blocks, block_to_block_type, BlockType, text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = len(block) - len(block.lstrip("#"))
    text = block.lstrip("# ").strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text = block.strip("```")
    if text.startswith("\n"):
        text = text[1:]
    # Don't strip the trailing newline - keep it as is
    children = [LeafNode(None, text)]
    return ParentNode("pre", [ParentNode("code", children)])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("> ").strip())
    quote_text = " ".join(new_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line.lstrip("- ").strip()
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line.lstrip("1234567890. ").strip()
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            html_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            html_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            html_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            html_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            html_node = ordered_list_to_html_node(block)
        else:
            raise ValueError(f"Invalid block type: {block_type}")
        
        children.append(html_node)
    
    return ParentNode("div", children)
