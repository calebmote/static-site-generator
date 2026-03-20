import unittest
from textnode import TextNode, textType
from text_operations import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", textType.CODE)
        
        expected = [
            TextNode("This is text with a ", textType.PLAIN),
            TextNode("code block", textType.CODE),
            TextNode(" word", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold(self):
        node = TextNode("This is **bold** text", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", textType.BOLD)
        
        expected = [
            TextNode("This is ", textType.PLAIN),
            TextNode("bold", textType.BOLD),
            TextNode(" text", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This is _italic_ text", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", textType.ITALIC)
        
        expected = [
            TextNode("This is ", textType.PLAIN),
            TextNode("italic", textType.ITALIC),
            TextNode(" text", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This has `code` and **bold** and _italic_", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", textType.CODE)
        
        expected = [
            TextNode("This has ", textType.PLAIN),
            TextNode("code", textType.CODE),
            TextNode(" and **bold** and _italic_", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("This is just plain text", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", textType.CODE)
        
        expected = [TextNode("This is just plain text", textType.PLAIN)]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at start", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", textType.BOLD)
        
        expected = [
            TextNode("bold", textType.BOLD),
            TextNode(" at start", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("bold at end **bold**", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", textType.BOLD)
        
        expected = [
            TextNode("bold at end ", textType.PLAIN),
            TextNode("bold", textType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_between_delimiters(self):
        node = TextNode("This has ** ** empty", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", textType.BOLD)
        
        expected = [
            TextNode("This has ", textType.PLAIN),
            TextNode(" ", textType.BOLD),
            TextNode(" empty", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes_unchanged(self):
        bold_node = TextNode("already bold", textType.BOLD)
        italic_node = TextNode("already italic", textType.ITALIC)
        new_nodes = split_nodes_delimiter([bold_node, italic_node], "`", textType.CODE)
        
        expected = [bold_node, italic_node]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("This has `unclosed code", textType.PLAIN)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", textType.CODE)
        self.assertIn("Invalid markdown syntax: unclosed delimiter", str(context.exception))

    def test_multiple_nodes(self):
        node1 = TextNode("First `code` node", textType.PLAIN)
        node2 = TextNode("Second **bold** node", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node1, node2], "`", textType.CODE)
        
        expected = [
            TextNode("First ", textType.PLAIN),
            TextNode("code", textType.CODE),
            TextNode(" node", textType.PLAIN),
            TextNode("Second **bold** node", textType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_consecutive_delimiters(self):
        node = TextNode("`code1``code2`", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", textType.CODE)
        
        expected = [
            TextNode("code1", textType.CODE),
            TextNode("code2", textType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_only_delimiters(self):
        node = TextNode("**", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", textType.BOLD)
        
        expected = [
            TextNode("", textType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_text(self):
        node = TextNode("", textType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", textType.CODE)
        
        expected = [TextNode("", textType.PLAIN)]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_images_with_special_chars(self):
        text = "This has an ![image with spaces and symbols!@#$%](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        expected = [("image with spaces and symbols!@#$%", "https://example.com/image.png")]
        self.assertListEqual(expected, matches)

    def test_extract_images_with_empty_alt(self):
        text = "This has an ![](https://example.com/image.png) image"
        matches = extract_markdown_images(text)
        expected = [("", "https://example.com/image.png")]
        self.assertListEqual(expected, matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_links(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_with_special_chars(self):
        text = "This has a [link with spaces and symbols!@#$%](https://example.com/page)"
        matches = extract_markdown_links(text)
        expected = [("link with spaces and symbols!@#$%", "https://example.com/page")]
        self.assertListEqual(expected, matches)

    def test_extract_links_with_empty_text(self):
        text = "This has an [](https://example.com) link"
        matches = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertListEqual(expected, matches)

    def test_extract_mixed_content(self):
        text = "Text with ![image](https://example.com/img.png) and [link](https://example.com/link)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("image", "https://example.com/img.png")], images)
        self.assertListEqual([("link", "https://example.com/link")], links)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            textType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", textType.PLAIN),
                TextNode("image", textType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", textType.PLAIN),
                TextNode(
                    "second image", textType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text with no images", textType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![image](https://example.com/img.png) at start", textType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", textType.IMAGE, "https://example.com/img.png"),
                TextNode(" at start", textType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("Image at end ![image](https://example.com/img.png)", textType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image at end ", textType.PLAIN),
                TextNode("image", textType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode("This has ![one image](https://example.com/img.png)", textType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has ", textType.PLAIN),
                TextNode("one image", textType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_non_text_node(self):
        node = TextNode("already bold", textType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_with_special_chars(self):
        node = TextNode("This has an ![image with spaces!@#$%](https://example.com/img.png)", textType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has an ", textType.PLAIN),
                TextNode("image with spaces!@#$%", textType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            textType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", textType.PLAIN),
                TextNode("to boot dev", textType.LINK, "https://www.boot.dev"),
                TextNode(" and ", textType.PLAIN),
                TextNode(
                    "to youtube", textType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is text with no links", textType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[link](https://example.com) at start", textType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", textType.LINK, "https://example.com"),
                TextNode(" at start", textType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("Link at end [link](https://example.com)", textType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link at end ", textType.PLAIN),
                TextNode("link", textType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode("This has [one link](https://example.com)", textType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has ", textType.PLAIN),
                TextNode("one link", textType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_non_text_node(self):
        node = TextNode("already italic", textType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_with_special_chars(self):
        node = TextNode("This has a [link with spaces!@#$%](https://example.com/page)", textType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a ", textType.PLAIN),
                TextNode("link with spaces!@#$%", textType.LINK, "https://example.com/page"),
            ],
            new_nodes,
        )

    def test_split_mixed_content(self):
        node = TextNode(
            "Text with ![image](https://example.com/img.png) and [link](https://example.com/link)",
            textType.PLAIN,
        )
        # Split images first
        image_nodes = split_nodes_image([node])
        # Then split links in the resulting text nodes
        final_nodes = []
        for img_node in image_nodes:
            if img_node.text_type == textType.PLAIN:
                final_nodes.extend(split_nodes_link([img_node]))
            else:
                final_nodes.append(img_node)
        
        expected = [
            TextNode("Text with ", textType.PLAIN),
            TextNode("image", textType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", textType.PLAIN),
            TextNode("link", textType.LINK, "https://example.com/link"),
        ]
        self.assertListEqual(expected, final_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", textType.PLAIN),
            TextNode("text", textType.BOLD),
            TextNode(" with an ", textType.PLAIN),
            TextNode("italic", textType.ITALIC),
            TextNode(" word and a ", textType.PLAIN),
            TextNode("code block", textType.CODE),
            TextNode(" and an ", textType.PLAIN),
            TextNode("obi wan image", textType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", textType.PLAIN),
            TextNode("link", textType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = [TextNode("", textType.PLAIN)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", textType.PLAIN)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", textType.PLAIN),
            TextNode("bold", textType.BOLD),
            TextNode(" text", textType.PLAIN),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_image(self):
        text = "This has an ![image](https://example.com/img.png) here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has an ", textType.PLAIN),
            TextNode("image", textType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", textType.PLAIN),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_link(self):
        text = "This has a [link](https://example.com) here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has a ", textType.PLAIN),
            TextNode("link", textType.LINK, "https://example.com"),
            TextNode(" here", textType.PLAIN),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_mixed_order(self):
        text = "Start `code` then **bold** then ![image](https://example.com/img.png) then [link](https://example.com) and _italic_ end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", textType.PLAIN),
            TextNode("code", textType.CODE),
            TextNode(" then ", textType.PLAIN),
            TextNode("bold", textType.BOLD),
            TextNode(" then ", textType.PLAIN),
            TextNode("image", textType.IMAGE, "https://example.com/img.png"),
            TextNode(" then ", textType.PLAIN),
            TextNode("link", textType.LINK, "https://example.com"),
            TextNode(" and ", textType.PLAIN),
            TextNode("italic", textType.ITALIC),
            TextNode(" end", textType.PLAIN),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_consecutive_formatting(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", textType.BOLD),
            TextNode("italic", textType.ITALIC),
            TextNode("code", textType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex(self):
        text = "Text with **bold** text and _italic_ text and `code` with ![image](https://example.com/img.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", textType.PLAIN),
            TextNode("bold", textType.BOLD),
            TextNode(" text and ", textType.PLAIN),
            TextNode("italic", textType.ITALIC),
            TextNode(" text and ", textType.PLAIN),
            TextNode("code", textType.CODE),
            TextNode(" with ", textType.PLAIN),
            TextNode("image", textType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", textType.PLAIN),
            TextNode("link", textType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
