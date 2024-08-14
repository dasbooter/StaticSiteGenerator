import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_core import markdown_to_html_node

def normalize_html(html):
    return html.replace('\n', '').replace(' ', '')

class TestHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n* List item 1\n* List item 2"
        html_node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><h1>Heading</h1><p>This is a paragraph.</p>"
            "<ul><li>List item 1</li><li>List item 2</li></ul></div>"
        )
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_simple_blockquote(self):
        markdown = "> This is a simple blockquote."
        html_node = markdown_to_html_node(markdown)
        expected_html = '<blockquote><p>This is a simple blockquote.</p></blockquote>'
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_multiline_blockquote(self):
        markdown = """> This is a multiline blockquote.
> It should handle multiple lines properly."""
        html_node = markdown_to_html_node(markdown)
        expected_html = '<blockquote><p>This is a multiline blockquote.\nIt should handle multiple lines properly.</p></blockquote>'
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_nested_blockquote(self):
        markdown = """> This is a blockquote with a nested blockquote.
> > This is the nested blockquote."""
        html_node = markdown_to_html_node(markdown)
        expected_html = ('<blockquote><p>This is a blockquote with a nested blockquote.</p>'
                         '<blockquote><p>This is the nested blockquote.</p></blockquote></blockquote>')
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_blockquote_with_other_elements(self):
        markdown = """> This blockquote contains **bold text** and *italic text*."""
        html_node = markdown_to_html_node(markdown)
        expected_html = '<blockquote><p>This blockquote contains <b>bold text</b> and <i>italic text</i>.</p></blockquote>'
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_blockquote_with_code(self):
        markdown = """> Here is a blockquote with some `inline code`."""
        html_node = markdown_to_html_node(markdown)
        expected_html = '<blockquote><p>Here is a blockquote with some <code>inline code</code>.</p></blockquote>'
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_blockquote_with_multiline_paragraph(self):
        markdown = """> This is a blockquote with a paragraph
> that spans multiple lines."""
        html_node = markdown_to_html_node(markdown)
        expected_html = '<blockquote><p>This is a blockquote with a paragraph\nthat spans multiple lines.</p></blockquote>'
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_blockquote_with_code_block(self):
        markdown = """> ```
> Blockquote with code block
> ```"""
        html_node = markdown_to_html_node(markdown)
        expected_html = ('<blockquote><pre><code>'
                         'Blockquote with code block'
                         '</code></pre></blockquote>')
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_complex_blockquote(self):
        markdown = """> This is a complex blockquote.
>
> - It has a list item
> - And another list item
> 
> And a paragraph at the end."""
        html_node = markdown_to_html_node(markdown)
        expected_html = ('<blockquote><p>This is a complex blockquote.</p>'
                         '<ul><li>It has a list item</li>'
                         '<li>And another list item</li></ul>'
                         '<p>And a paragraph at the end.</p></blockquote>')
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraph(self):
        block = "This is a simple paragraph."
        html_node = markdown_to_html_node(block)
        expected_html = "<div><p>This is a simple paragraph.</p></div>"
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_heading(self):
        block = "# This is a heading"
        html_node = markdown_to_html_node(block)
        expected_html = "<div><h1>This is a heading</h1></div>"
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_code_block(self):
        block = "```\ncode block\n```"
        html_node = markdown_to_html_node(block)
        expected_html = "<div><pre><code>\ncode block\n</code></pre></div>"
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_quote(self):
        markdown = "> All that is gold does not glitter"
        html_node = markdown_to_html_node(markdown)
        expected_html = '<blockquote><p>All that is gold does not glitter</p></blockquote>'
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        html_node = markdown_to_html_node(block)
        expected_html = (
            "<div><ul>"
            "<li>Item 1</li>"
            "<li>Item 2</li>"
            "</ul></div>"
        )
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

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
        self.assertEqual(normalize_html(html_node.to_html()), normalize_html(expected_html))

if __name__ == "__main__":
    unittest.main()
