import unittest

from textnode import TextNode


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

    #def test_not_equal_different_type(self):
        #node = TextNode("This is a text node", "bold")
        #not_a_textnode = "This is a string, not a TextNode"
        #self.assertNotEqual(node, not_a_textnode)

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

if __name__ == "__main__":
    unittest.main()
