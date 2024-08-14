from markdown_utilities import copy_static_files
from markdown_core import generate_pages_recursive

import os

def main():
    # Define paths
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template_path = "template.html"

    # Clear public directory if it exists
    if os.path.exists(public_dir):
        for root, dirs, files in os.walk(public_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    # Copy static files
    copy_static_files(static_dir, public_dir)

    # Generate HTML pages recursively
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()
