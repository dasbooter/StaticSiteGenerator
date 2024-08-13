import re
from markdown_utilities import extract_markdown_images, extract_markdown_links
from htmlnode import LeafNode  # Importing LeafNode for conversion purposes

class TextNode:
    def __init__(self, text, text_type, url=None, alt_text=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.alt_text = alt_text

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt_text, url in images:
            sections = current_text.split(f"![{alt_text}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], "text"))
            new_nodes.append(TextNode(alt_text, "image", url))
            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, "text"))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        for anchor_text, url in links:
            sections = current_text.split(f"[{anchor_text}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], "text"))
            new_nodes.append(TextNode(anchor_text, "link", url))
            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, "text"))

    return new_nodes
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        split_parts = node.text.split(delimiter)
        if len(split_parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        for i, part in enumerate(split_parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, "text"))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(value=text_node.text)
    
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    
    elif text_node.text_type == "link":
        if text_node.url is None:
            raise ValueError("Link nodes require a URL.")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    
    elif text_node.text_type == "image":
        if text_node.url is None:
            raise ValueError("Image nodes require a URL.")
        if text_node.alt_text is None:
            text_node.alt_text = ""
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.alt_text})
    
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    
    nodes = split_nodes_delimiter(nodes, "**", "bold")  # Handle bold (**)
    nodes = split_nodes_delimiter(nodes, "*", "italic")  # Handle italic (*)
    nodes = split_nodes_delimiter(nodes, "`", "code")  # Handle code (`)
    nodes = split_nodes_image(nodes)  # Handle images (![alt](url))
    nodes = split_nodes_link(nodes)  # Handle links ([text](url))

    return nodes

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in raw_blocks]
    blocks = [block for block in blocks if block]
    return blocks

def block_to_block_type(block):
    if block.startswith("#") and block.lstrip("#").startswith(" "):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if all(line.startswith(">") for line in block.splitlines()):
        return "quote"
    if all(line.startswith(("*", "-")) and line[1:2] == " " for line in block.splitlines()):
        return "unordered_list"
    lines = block.splitlines()
    if all(line.split(". ", 1)[0].isdigit() and line.split(". ", 1)[1] for line in lines):
        numbers = [int(line.split(". ", 1)[0]) for line in lines]
        if numbers == list(range(1, len(lines) + 1)):
            return "ordered_list"
    return "paragraph"
