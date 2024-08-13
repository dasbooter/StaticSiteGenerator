from markdown_utilities import extract_markdown_images, extract_markdown_links
from textnode import text_to_textnodes, block_to_block_type, markdown_to_blocks, text_node_to_html_node
from htmlnode import ParentNode, LeafNode

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]

def create_paragraph_node(block):
    return ParentNode(tag="p", children=text_to_children(block))

def create_heading_node(block, level):
    return ParentNode(tag=f"h{level}", children=text_to_children(block.lstrip("#").strip()))

def create_code_block_node(block):
    return ParentNode(tag="pre", children=[ParentNode(tag="code", children=[LeafNode(value=block.strip("`"))])])

def create_quote_node(block):
    content = "\n".join([line.lstrip("> ").strip() for line in block.splitlines()])
    return ParentNode(tag="blockquote", children=[create_paragraph_node(content)])

def create_unordered_list_node(block):
    list_items = block.splitlines()
    children = [ParentNode(tag="li", children=text_to_children(item[2:].strip())) for item in list_items]
    return ParentNode(tag="ul", children=children)

def create_ordered_list_node(block):
    list_items = block.splitlines()
    children = [ParentNode(tag="li", children=text_to_children(item.split(". ", 1)[1].strip())) for item in list_items]
    return ParentNode(tag="ol", children=children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "heading":
        level = len(block.split()[0])  # Number of # characters
        return create_heading_node(block, level)
    elif block_type == "code":
        return create_code_block_node(block)
    elif block_type == "quote":
        return create_quote_node(block)
    elif block_type == "unordered_list":
        return create_unordered_list_node(block)
    elif block_type == "ordered_list":
        return create_ordered_list_node(block)
    else:  # Paragraph
        return create_paragraph_node(block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode(tag="div", children=block_nodes)
