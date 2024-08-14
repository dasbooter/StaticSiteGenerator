import os
from markdown_utilities import extract_title
from textnode import text_to_textnodes, block_to_block_type, markdown_to_blocks, text_node_to_html_node
from htmlnode import ParentNode, LeafNode, HTMLNode

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]

def create_paragraph_node(block):
    children = text_to_children(block)
    if children:
        return ParentNode(tag="p", children=children)
    return LeafNode(value="")  # Return an empty LeafNode to avoid returning None

def create_heading_node(block, level):
    return ParentNode(tag=f"h{level}", children=text_to_children(block.lstrip("#").strip()))

def create_code_block_node(block):
    content = block.strip("`")
    return ParentNode(tag="pre", children=[ParentNode(tag="code", children=[LeafNode(value=content)])])

def create_quote_node(block):
    lines = block.splitlines()
    paragraphs = []
    current_paragraph = []
    inside_code_block = False
    code_block_content = []
    nested_quote = []
    list_items = []

    for line in lines:
        stripped_line = line.lstrip("> ").strip()

        if stripped_line.startswith("```"):
            if inside_code_block:
                code_block_content.append(stripped_line)
                paragraphs.append(create_code_block_node("\n".join(code_block_content)))
                code_block_content = []
                inside_code_block = False
            else:
                inside_code_block = True
                code_block_content.append(stripped_line)
            continue

        if inside_code_block:
            code_block_content.append(stripped_line)
            continue

        if line.startswith("> >"):
            nested_quote.append(line[2:])
            continue

        if nested_quote:
            paragraphs.append(create_quote_node("\n".join(nested_quote)))
            nested_quote = []

        if stripped_line.startswith(("* ", "- ")):
            list_items.append(stripped_line)
            continue

        if list_items:
            paragraphs.append("\n".join(list_items))
            list_items = []

        if stripped_line:
            current_paragraph.append(stripped_line)
        else:
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []

    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))
    if list_items:
        paragraphs.append("\n".join(list_items))
    if nested_quote:
        paragraphs.append(create_quote_node("\n".join(nested_quote)))

    # If there's only one paragraph, return it directly without wrapping it in a <p> tag
    if len(paragraphs) == 1:
        return LeafNode(tag="blockquote", value=paragraphs[0])

    children = []
    for p in paragraphs:
        if isinstance(p, str) and (p.startswith("* ") or p.startswith("- ")):
            children.append(create_unordered_list_node(p))
        elif isinstance(p, str):
            children.append(create_paragraph_node(p))
        else:
            children.append(p)

    if children:
        return ParentNode(tag="blockquote", children=children)
    return LeafNode(value="")  # Return an empty LeafNode to avoid returning None

def create_unordered_list_node(block):
    items = block.splitlines()
    children = [
        ParentNode(tag="li", children=text_to_children(item[2:].strip()))
        for item in items if item.startswith(("* ", "- "))
    ]
    if children:
        return ParentNode(tag="ul", children=children)
    return LeafNode(value="")  # Return an empty LeafNode to avoid returning None

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
        return create_quote_node(block)  # Directly return the quote node
    elif block_type == "unordered_list":
        return create_unordered_list_node(block)
    elif block_type == "ordered_list":
        return create_ordered_list_node(block)
    else:  # Paragraph
        return create_paragraph_node(block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = [block_to_html_node(block) for block in blocks]
    
    # Only wrap in a <div> if needed
    if len(block_nodes) == 1 and isinstance(block_nodes[0], ParentNode) and block_nodes[0].tag == "blockquote":
        return block_nodes[0]
    
    return ParentNode(tag="div", children=block_nodes)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    final_content = template_content.replace("{{ Title }}", title)
    final_content = template_content.replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_content)

    print(f"Page generated at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, dir_path_content)
                dest_path_dir = os.path.join(dest_dir_path, rel_path)
                os.makedirs(dest_path_dir, exist_ok=True)
                dest_path = os.path.join(dest_path_dir, file.replace('.md', '.html'))
                generate_page(from_path, template_path, dest_path)
