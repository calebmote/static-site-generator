import unittest
from text_operations import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")
        
        md = "#   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")
        
        md = "# This is a title"
        self.assertEqual(extract_title(md), "This is a title")

    def test_extract_title_with_content_after(self):
        md = """# Title

This is some content after the title.
"""
        self.assertEqual(extract_title(md), "Title")

    def test_extract_title_no_h1(self):
        md = "## This is h2"
        with self.assertRaises(ValueError):
            extract_title(md)
        
        md = "This is just text"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_empty(self):
        md = ""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_mixed_content(self):
        md = """
# Main Title

Some content here

## Subheading

More content
"""
        self.assertEqual(extract_title(md), "Main Title")


if __name__ == "__main__":
    unittest.main()
