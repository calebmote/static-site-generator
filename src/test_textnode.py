import unittest
from textnode import TextNode, textType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", textType.BOLD)
        node2 = TextNode("This is a text node", textType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", textType.BOLD)
        node2 = TextNode("This is a different text node", textType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", textType.BOLD)
        node2 = TextNode("This is a text node", textType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", textType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", textType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("This is a text node", textType.BOLD)
        node2 = TextNode("This is a text node", textType.BOLD, None)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", textType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", textType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_different_types(self):
        node = TextNode("This is a text node", textType.BOLD)
        self.assertNotEqual(node, "not a TextNode")

    def test_repr(self):
        node = TextNode("test", textType.BOLD, "https://example.com")
        self.assertEqual(repr(node), "TextNode(test, textType.BOLD, https://example.com)")

    def test_repr_no_url(self):
        node = TextNode("test", textType.BOLD)
        self.assertEqual(repr(node), "TextNode(test, textType.BOLD, None)")

    def test_eq_url_vs_none(self):
        node = TextNode("test", textType.LINK, "https://example.com")
        node2 = TextNode("test", textType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_eq_all_text_types(self):
        text = "test text"
        for text_type in [textType.PLAIN, textType.BOLD, textType.ITALIC, textType.CODE, textType.LINK, textType.IMAGE]:
            node1 = TextNode(text, text_type)
            node2 = TextNode(text, text_type)
            self.assertEqual(node1, node2)

    def test_eq_empty_text(self):
        node = TextNode("", textType.BOLD)
        node2 = TextNode("", textType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_empty_url(self):
        node = TextNode("test", textType.LINK, "")
        node2 = TextNode("test", textType.LINK, "")
        self.assertEqual(node, node2)

    def test_eq_empty_vs_none_url(self):
        node = TextNode("test", textType.LINK, "")
        node2 = TextNode("test", textType.LINK, None)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", textType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", textType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("Italic text", textType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("Code text", textType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Click me", textType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image(self):
        node = TextNode("Alt text", textType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "Alt text"})

    def test_link_no_url(self):
        node = TextNode("Click me", textType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link TextNode must have a URL")

    def test_image_no_url(self):
        node = TextNode("Alt text", textType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image TextNode must have a URL")

    def test_invalid_input(self):
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node("not a TextNode")
        self.assertEqual(str(context.exception), "Input must be a TextNode")

    def test_unsupported_text_type(self):
        # Create a mock TextNode with invalid type
        node = TextNode("test", "invalid_type")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported text type", str(context.exception))


if __name__ == "__main__":
    unittest.main()