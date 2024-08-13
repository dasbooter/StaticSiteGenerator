from markdown_utilities import copy_static_files
from markdown_core import generate_page

import os

def main():
    # Define paths
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template_path = "template.html"
    output_path = os.path.join(public_dir, "index.html")

    # Copy static files
    copy_static_files(static_dir, public_dir)

    # Generate the HTML page
    generate_page(os.path.join(content_dir, "index.md"), template_path, output_path)

if __name__ == "__main__":
    main()
