# test_parentnode.py

import unittest
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestParentNode(unittest.TestCase):

    def test_parent_node_with_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Hello"),
                LeafNode(None, " "),
                LeafNode("strong", "World")
            ]
        )
        expected_html = "<div><span>Hello</span> <strong>World</strong></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_no_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("span", "Hello")])
        self.assertEqual(str(context.exception), "ParentNode must have a tag.")

    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])
        self.assertEqual(str(context.exception), "ParentNode must have children.")

    def test_nested_parent_node(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text")
                    ]
                ),
                LeafNode("hr", None, {"style": "border:none;"})
            ]
        )
        expected_html = "<div><p><b>Bold text</b>Normal text</p><hr style=\"border:none;\" /></div>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == '__main__':
    unittest.main()
