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
        if isinstance(node, TextNode):
            text = node.text
            current_type = node.text_type
        else:
            #If node is not a TextNode, create a new TextNode
            text = str(node)
            current_type = text_type_text
            node = TextNode(text, current_type)
        if delimiter == '*':
            if '*' in text:
                italic_split = re.split(r'(\*.*?(\*|$))', text)
                new_nodes.extend(delimiter_helper(italic_split, '*', text_type_italic))
            else:
                new_nodes.append(node)
        elif delimiter == "**":
            if '**' in text:
                bold_split = re.split(r'(\*\*.*?(\*\*|$))', text)
                new_nodes.extend(delimiter_helper(bold_split, "**", text_type_bold))
            else:
                new_nodes.append(node)
        elif delimiter == "`":
            #if '`' in node.text:
            if "`" in text:
                code_split = re.split(r'(\`.*?(\`|$))', text)
                new_nodes.extend(delimiter_helper(code_split, "`", text_type_code))
            else:
                new_nodes.append(node)

    #print(new_nodes)
    return new_nodes

def delimiter_helper(split_text, delimiter, text_type):
    new_nodes = []

    #Calculate the length of delimiter to extract the text inside
    delimiter_len = len(delimiter)

    for part in split_text:
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
            #text_node_list.append(TextNode(alt_text, text_type_image, url))
            return TextNode(alt_text, text_type_image, url)
        elif text_type == text_type_link:
            text = item[0]
            url = item[1]
            #text_node_list.append(TextNode(text, text_type_link, url))
            return TextNode(text, text_type_link, url)

    #return text_node_list


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if not extract_markdown_images(node.text):
            new_nodes.append(node)
        else:
            remaining_text = node.text
            while extract_markdown_images(remaining_text):
                tuple_holder = extract_markdown_images(remaining_text)[0]
                full_image_markdown = f'![{tuple_holder[0]}]({tuple_holder[1]})'
                parts = remaining_text.split(full_image_markdown, 1)

                # Add text before image if it exists
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                
                # Add image node
                new_nodes.append(extract_markdown_converter([tuple_holder], text_type_image))

                # Update remaining_text for next iteration
                remaining_text = parts[1] if len(parts) > 1 else ""
            
            # Add any remaining text after last image
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if not extract_markdown_links(node.text):
            new_nodes.append(node)
        else:
            remaining_text = node.text
            while extract_markdown_links(remaining_text):
                tuple_holder = extract_markdown_links(remaining_text)[0]
                full_link_markdown = f'[{tuple_holder[0]}]({tuple_holder[1]})'
                parts = remaining_text.split(full_link_markdown, 1)

                # Add text before link if it exists
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                
                # Add link node
                new_nodes.append(extract_markdown_converter([tuple_holder], text_type_link))

                # Update remaining_text for next iteration
                remaining_text = parts[1] if len(parts) > 1 else ""
            
            # Add any remaining text after last link
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]

    #Split for bold
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    #Split for italic
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    #Split for code
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    #Split for images
    nodes = split_nodes_image(nodes)
    #Split for links
    nodes = split_nodes_link(nodes)

    return nodes
