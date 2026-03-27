import unittest
from markdown_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is a level 1 heading

## This is a level 2 heading

### This is a level 3 heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a level 1 heading</h1><h2>This is a level 2 heading</h2><h3>This is a level 3 heading</h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with multiple lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_mixed_content(self):
        md = """
# Heading

This is a paragraph with **bold** and _italic_ text.

> This is a quote
> with multiple lines

- List item 1
- List item 2

```
Code block
with no formatting
```

Final paragraph.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><blockquote>This is a quote with multiple lines</blockquote><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>Code block\nwith no formatting\n</code></pre><p>Final paragraph.</p></div>",
        )

    def test_inline_formatting_in_lists(self):
        md = """
- **Bold** list item
- _Italic_ list item
- `Code` list item
- [Link](https://example.com) list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>Bold</b> list item</li><li><i>Italic</i> list item</li><li><code>Code</code> list item</li><li><a href=\"https://example.com\">Link</a> list item</li></ul></div>",
        )

    def test_inline_formatting_in_quotes(self):
        md = """
> This quote has **bold** text
> and _italic_ text
> and `code` text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This quote has <b>bold</b> text and <i>italic</i> text and <code>code</code> text</blockquote></div>",
        )

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_single_paragraph(self):
        md = "This is a single paragraph"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a single paragraph</p></div>")


if __name__ == "__main__":
    unittest.main()
