# test_textnode.py

import unittest
from textnode import TextNode, text_to_textnodes, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, markdown_to_blocks, block_to_block_type
from markdown_utilities import extract_markdown_images, extract_markdown_links, extract_title


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_equal_different_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_equal_with_url(self):
        node = TextNode("This is a text node", "bold", "https://www.example.com")
        node2 = TextNode("This is a text node", "bold", "https://www.example.com")
        self.assertEqual(node, node2)

    def test_not_equal_different_url(self):
        node = TextNode("This is a text node", "bold", "https://www.example.com")
        node2 = TextNode("This is a text node", "bold", "https://www.anotherexample.com")
        self.assertNotEqual(node, node2)

    def test_equal_none_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_not_equal_empty_string(self):
        node = TextNode("", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", "")
        self.assertNotEqual(node3, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        expected_repr = "TextNode(This is a text node, bold, https://www.boot.dev)"
        self.assertEqual(repr(node), expected_repr)

    def test_default_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    def test_not_equal_with_and_without_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_equal_case_sensitive(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a TEXT node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_equal_case_sensitive_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.BOOT.dev")
        self.assertNotEqual(node, node2)  # assuming URLs are case-sensitive

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text_type_text(self):
        text_node = TextNode(text_type="text", text="Some text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Some text")

    def test_text_type_bold(self):
        text_node = TextNode(text_type="bold", text="Bold text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_type_italic(self):
        text_node = TextNode(text_type="italic", text="Italic text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_type_code(self):
        text_node = TextNode(text_type="code", text="print('Hello')")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_text_type_link(self):
        text_node = TextNode(text_type="link", text="Click here", url="https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.example.com">Click here</a>')

    def test_text_type_invalid(self):
        text_node = TextNode(text_type="unknown", text="Unknown type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_simple_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_text(self):
        node = TextNode("This is **bold** text", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_text(self):
        node = TextNode("This is *italic* text", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_with_unmatched_delimiter_raises_error(self):
        node = TextNode("This is a `broken code block", "text")
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", "code")
        self.assertEqual(str(context.exception), "Unmatched delimiter '`' in text: This is a `broken code block")

    def test_no_split_needed(self):
        node = TextNode("This is plain text.", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        expected = [node]
        self.assertEqual(new_nodes, expected)

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_match(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_match(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_images_and_links_mixed(self):
        text = "![image1](https://image.com/1.png) and [link1](https://link.com) with ![image2](https://image.com/2.png) and [link2](https://link2.com)"
        expected_images = [
            ("image1", "https://image.com/1.png"),
            ("image2", "https://image.com/2.png")
        ]
        expected_links = [
            ("link1", "https://link.com"),
            ("link2", "https://link2.com")
        ]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![alt text](https://image.com/image.png) and more text",
            "text"
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an image ", "text"),
            TextNode("alt text", "image", "https://image.com/image.png"),
            TextNode(" and more text", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and more text",
            "text"
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and more text", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_split_image(self):
        node = TextNode("This is plain text with no images.", "text")
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_no_split_link(self):
        node = TextNode("This is plain text with no links.", "text")
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_and_link(self):
        node = TextNode(
            "Text with an image ![img](https://image.com/1.png) and a link [link](https://link.com)",
            "text"
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        expected = [
            TextNode("Text with an image ", "text"),
            TextNode("img", "image", "https://image.com/1.png"),
            TextNode(" and a link ", "text"),
            TextNode("link", "link", "https://link.com"),
        ]
        self.assertEqual(new_nodes, expected)

class TestTextToTextNodes(unittest.TestCase):

    def test_simple_text(self):
        text = "This is simple text."
        expected = [TextNode("This is simple text.", "text")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text.", "text")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        expected = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text.", "text")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        text = "This is `code`."
        expected = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(".", "text")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "This is an image ![alt text](https://image.com/img.png)."
        expected = [
            TextNode("This is an image ", "text"),
            TextNode("alt text", "image", "https://image.com/img.png"),
            TextNode(".", "text")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "This is a [link](https://link.com)."
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://link.com"),
            TextNode(".", "text")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_combined_text(self):
        text = "This is **bold** text with *italic* and `code`."
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text with ", "text"),
            TextNode("italic", "italic"),
            TextNode(" and ", "text"),
            TextNode("code", "code"),
            TextNode(".", "text")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_complex_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_heading(self):
        markdown = "# This is a heading"
        expected = ["# This is a heading"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_paragraph(self):
        markdown = "This is a single paragraph of text."
        expected = ["This is a single paragraph of text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blocks(self):
        markdown = """# Heading

This is a paragraph of text.

* List item 1
* List item 2
"""
        expected = [
            "# Heading",
            "This is a paragraph of text.",
            "* List item 1\n* List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_trailing_whitespace(self):
        markdown = "   # Heading   \n\n   This is a paragraph with trailing whitespace.   "
        expected = ["# Heading", "This is a paragraph with trailing whitespace."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_blocks(self):
        markdown = "# Heading\n\n\n\nThis is a paragraph.\n\n\n\n* List item"
        expected = [
            "# Heading",
            "This is a paragraph.",
            "* List item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_no_blocks(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")

        block = "## This is a subheading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code_block(self):
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_quote_block(self):
        block = "> This is a quote\n> block"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_unordered_list(self):
        block = "* List item 1\n* List item 2"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        
        block = "- List item 1\n- List item 2"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), "paragraph")

        block = "This is a paragraph with multiple lines.\nIt should still be recognized as a paragraph."
        self.assertEqual(block_to_block_type(block), "paragraph")

class TestExtractTitle(unittest.TestCase):

    def test_extract_title_with_h1(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_extra_whitespace(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_no_h1(self):
        markdown = "## Hello World"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
