import shutil
import os

from functional_textnode import markdown_to_html_node
from htmlnode import *

def main():
    copy_static("static", "public")


def copy_static(src_path, dest_path):
    # Check if destination exists before removing
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    
    # Create the new destination directory
    os.mkdir(dest_path)

    # List of contents of source directory
    dir_list = os.listdir(src_path)

    for entry in dir_list:
        # Create full paths
        src_entry = os.path.join(src_path, entry)
        dest_entry = os.path.join(dest_path, entry)

        if os.path.isfile(src_entry):
            print(f"Copying file: {src_entry}")
            shutil.copy(src_entry, dest_entry)
        elif os.path.isdir(src_entry):
            print(f"Copying directory: {src_entry}")
            copy_static(src_entry, dest_entry)

def extract_title(markdown):
    lines = markdown.split('\n')

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            h1_header = stripped_line[1:]
            stripped_header = h1_header.strip()
            return stripped_header
        
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Open and read the files that paths lead to
    with open(from_path) as markdown_file:
        markdown_content = markdown_file.read()
    
    with open(template_path) as template_file:
        template_content = template_file.read()

    # Convert file contents to html
    html_nodes = markdown_to_html_node(markdown_content)
    html_string = html_nodes.to_html()

    # Get title
    title = extract_title(markdown_content)

    # Store the results of replacements for title and content placeholders
    result = template_content.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_string)

    # Check to ensure directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Open in write mode and write the result
    with open(dest_path, "w") as dest_file:
        dest_file.write(result)




if __name__ == "__main__":
    main()
