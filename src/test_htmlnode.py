import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
