from enum import Enum
from htmlnode import LeafNode

class textType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode")
    
    if text_node.text_type == textType.PLAIN:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == textType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == textType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == textType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == textType.LINK:
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == textType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")

def main():
    node = TextNode("This is some anchor text", textType.PLAIN)
    print(node)

if __name__ == "__main__":
    main()