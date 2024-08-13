# test_leafnode.py

import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_leafnode_without_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p")

    def test_leafnode_to_html_with_tag(self):
        node = LeafNode(tag="p", value="This is a paragraph.")
        expected_html = "<p>This is a paragraph.</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_to_html_without_tag(self):
        node = LeafNode(value="This is raw text.")
        expected_html = "This is raw text."
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        expected_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
