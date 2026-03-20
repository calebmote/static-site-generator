import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        self.assertEqual(repr(node), "HTMLNode(p, Hello, None, {'class': 'text'})")

    def test_repr_all_none(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("div", "Content", {"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), '<div class="container" id="main">Content</div>')

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, {'class': 'text'})")

    def test_leaf_repr_no_props(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(repr(node), "LeafNode(p, Hello, None)")

if __name__ == "__main__":
    unittest.main()

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_to_html_with_props(self):
        node = ParentNode("div", [
            LeafNode("span", "Hello"),
            LeafNode("span", "World")
        ], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>Hello</span><span>World</span></div>')

    def test_parent_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_parent_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_parent_nested(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("b", "Hello"),
                LeafNode(None, " ")
            ]),
            ParentNode("p", [
                LeafNode("i", "World")
            ])
        ])
        self.assertEqual(node.to_html(), "<div><p><b>Hello</b> </p><p><i>World</i></p></div>")

    def test_parent_repr(self):
        node = ParentNode("div", [LeafNode("p", "text")], {"class": "container"})
        self.assertEqual(repr(node), "ParentNode(div, [LeafNode(p, text, None)], {'class': 'container'})")

    def test_parent_repr_no_props(self):
        node = ParentNode("div", [LeafNode("p", "text")])
        self.assertEqual(repr(node), "ParentNode(div, [LeafNode(p, text, None)], None)")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_parent_multiple_children_mixed(self):
        node = ParentNode("body", [
            LeafNode("h1", "Title"),
            ParentNode("p", [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic")
            ]),
            LeafNode(None, "Raw text"),
            ParentNode("div", [
                LeafNode("span", "Nested")
            ])
        ])
        expected = "<body><h1>Title</h1><p><b>Bold</b> and <i>italic</i></p>Raw text<div><span>Nested</span></div></body>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_deeply_nested(self):
        node = ParentNode("html", [
            ParentNode("head", [
                ParentNode("title", [
                    LeafNode(None, "Page Title")
                ])
            ]),
            ParentNode("body", [
                ParentNode("div", [
                    ParentNode("p", [
                        LeafNode("span", "Deeply nested content")
                    ])
                ])
            ])
        ])
        expected = "<html><head><title>Page Title</title></head><body><div><p><span>Deeply nested content</span></p></div></body></html>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_with_props_and_children(self):
        node = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ], {"class": "list", "id": "main-list"})
        expected = '<ul class="list" id="main-list"><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'
        self.assertEqual(node.to_html(), expected)

    def test_parent_children_with_raw_text(self):
        node = ParentNode("p", [
            LeafNode(None, "Start "),
            LeafNode("b", "bold"),
            LeafNode(None, " middle "),
            LeafNode("i", "italic"),
            LeafNode(None, " end")
        ])
        expected = "<p>Start <b>bold</b> middle <i>italic</i> end</p>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_single_leaf_child(self):
        node = ParentNode("div", [LeafNode(None, "Just text")])
        self.assertEqual(node.to_html(), "<div>Just text</div>")

    def test_parent_children_with_props(self):
        node = ParentNode("form", [
            LeafNode("button", "Submit", {"type": "submit"}),
            LeafNode("textarea", "Enter text here", {"name": "message"})
        ], {"method": "post", "action": "/submit"})
        expected = '<form method="post" action="/submit"><button type="submit">Submit</button><textarea name="message">Enter text here</textarea></form>'
        self.assertEqual(node.to_html(), expected)

    def test_parent_children_empty_values(self):
        node = ParentNode("div", [
            LeafNode("span", ""),
            LeafNode(None, ""),
            LeafNode("p", "Not empty")
        ])
        expected = "<div><span></span><p>Not empty</p></div>"
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()
