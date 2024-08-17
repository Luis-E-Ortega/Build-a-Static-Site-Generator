import re

from textnode import TextNode

#Create identifiers for each type of delimiter
text_type_text='text'
text_type_bold='bold'
text_type_italic='italic'
text_type_code='code'
text_type_link='link'
text_type_image='image'

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #Empty list to store split nodes into
    new_nodes = []

    for node in old_nodes:
        if delimiter == '*':
            if '*' in node.text:
                italic_split = re.split(r'(\*.*?(\*|$))', node.text)
                new_nodes.extend(delimiter_helper(italic_split, '*', text_type_italic))
            else:
                new_nodes.extend(node.text)
        elif delimiter == "**":
            if '**' in node.text:
                bold_split = re.split(r'(\*\*.*?(\*\*|$))', node.text)
                new_nodes.extend(delimiter_helper(bold_split, "**", text_type_bold))
            else:
                new_nodes.extend(node.text)
        elif delimiter == "`":
            if '`' in node.text:
                code_split = re.split(r'(\`.*?(\`|$))', node.text)
                new_nodes.extend(delimiter_helper(code_split, "`", text_type_code))
            else:
                new_nodes.extend(node.text)

    #print(new_nodes)
    return new_nodes

def delimiter_helper(split, delimiter, text_type):
    new_nodes = []

    #Calculate the length of delimiter to extract the text inside
    delimiter_len = len(delimiter)

    for part in split:
        if part.strip(delimiter).strip() == '':
            continue
        if part.startswith(delimiter) and part.endswith(delimiter):
            new_nodes.append(TextNode(part[delimiter_len:-delimiter_len], text_type))
        elif part.startswith(delimiter) and not part.endswith(delimiter):
            raise ValueError("Must have matching delimiters")
        elif not part.startswith(delimiter) and part.endswith(delimiter):
            raise ValueError("Must have matching delimiters")
        else:
            new_nodes.append(TextNode(part, text_type_text))
    return new_nodes



def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    links_image = re.findall(pattern, text)
    return links_image

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    links_standard = re.findall(pattern, text)
    return links_standard


def extract_markdown_converter(tuples, text_type):
    text_node_list = []

    for item in tuples:
        if text_type == text_type_image:
            alt_text = item[0]
            url = item[1]
            text_node_list.append(TextNode(alt_text, text_type_image, url))
        elif text_type == text_type_link:
            text = item[0]
            url = item[1]
            text_node_list.append(TextNode(text, text_type_link, url))

    return text_node_list


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text == '':
            continue
        if not extract_markdown_images(node.text):
            new_nodes.append(node)
        else:
            for tuple in extract_markdown_images(node.text):
                
            new_nodes.append(extract_markdown_images(node.text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text == '':
            continue
        if not extract_markdown_links(node.text):
            new_nodes.append(node)
        else:
            new_nodes.append(extract_markdown_links(node.text))
    return new_nodes
