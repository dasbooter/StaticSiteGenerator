# test_htmlnode.py

import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_core import markdown_to_html_node

class TestHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n* List item 1\n* List item 2"
        html_node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><h1>Heading</h1><p>This is a paragraph.</p>"
            "<ul><li>List item 1</li><li>List item 2</li></ul></div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_attributes(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_repr(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.google.com"})
        expected_repr = ("HTMLNode(tag=a, value=Click here, children=[], "
                         "props={'href': 'https://www.google.com'})")
        self.assertEqual(repr(node), expected_repr)

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraph(self):
        block = "This is a simple paragraph."
        html_node = markdown_to_html_node(block)
        expected_html = "<div><p>This is a simple paragraph.</p></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_heading(self):
        block = "# This is a heading"
        html_node = markdown_to_html_node(block)
        expected_html = "<div><h1>This is a heading</h1></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_code_block(self):
        block = "```\ncode block\n```"
        html_node = markdown_to_html_node(block)
        expected_html = "<div><pre><code>\ncode block\n</code></pre></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_quote(self):
        block = "> This is a quote"
        html_node = markdown_to_html_node(block)
        expected_html = "<div><blockquote><p>This is a quote</p></blockquote></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        html_node = markdown_to_html_node(block)
        expected_html = (
            "<div><ul>"
            "<li>Item 1</li>"
            "<li>Item 2</li>"
            "</ul></div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(block)
        expected_html = (
            "<div><ol>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li>Third item</li>"
            "</ol></div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
