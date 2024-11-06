import re

from textnode import TextNode
from blocks import markdown_to_blocks, block_to_block_type
from htmlnode import *

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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    

    for block in blocks:
        block_type = block_to_block_type(block) 
        node = None #Initializing the node to be reused for each case
        match block_type:
            case "code":
                node = block_to_code_node(block)
            case "heading":
                node = block_to_heading_node(block)
            case "quote":
                node = block_to_quote_node(block)
            case "unordered_list":
                node = block_to_unordered_list_node(block)
            case "ordered_list":
                node = block_to_ordered_list_node(block)
            case "paragraph":
                node = block_to_paragraph_node(block)
        if node:
            child_nodes.append(node)
    root_node = HTMLNode("div")
    root_node.children = child_nodes
    return root_node

def block_to_code_node(block):
    code_content = block.strip('`')
    code_node = HTMLNode("code", [HTMLNode("text", code_content)])
    return HTMLNode("pre", [code_node])

def block_to_heading_node(block):
    heading_level = block.count('#') # Counts how many '#' at the start
    heading_content = block.strip("#").strip() # This removes the '#' and extra spaces
    tag = f"h{heading_level}" # Creates correct HTML tag based on level
    return HTMLNode(tag, [HTMLNode("text", heading_content)])

def block_to_quote_node(block):
    lines = block.split("\n")
    quote_content = "\n".join(line.lstrip("> ").strip() for line in lines)
    return HTMLNode("blockquote", [HTMLNode("text", quote_content)])

def block_to_unordered_list_node(block):
    li_list = []
    unordered_list_nodes = []

    line_split = block.split("\n")
    for line in line_split:
        if (line.startswith("* ") or line.startswith("- ")):
            li_list.append(line)
        else:
            if li_list:
                li_list[-1] += "\n" + line
    for list_element in li_list:
        unordered_list_nodes.append(HTMLNode("li", [HTMLNode("text", list_element)]))
    return (HTMLNode("ul", children=unordered_list_nodes))

def block_to_ordered_list_node(block):
    li_list = []
    ordered_list_nodes = []

    line_split = block.split("\n")
    for line in line_split:
        if re.match(r"^\d+\.\s", line): # Checks if the line starts with "number. "
            li_list.append(line)
        else:
            if li_list:
                li_list[-1] += "\n" + line
    for list_element in li_list:
        # Strip the numbering from the start of the line
        clean_element = re.sub(r"^\d+\.\s", "", list_element)
        ordered_list_nodes.append(HTMLNode("li", [HTMLNode("text", clean_element)]))

    return (HTMLNode("ol", children=ordered_list_nodes))

def block_to_paragraph_node(block):
    paragraph_content = block.strip()
    return HTMLNode("p", [HTMLNode("text", paragraph_content)])


def text_to_children(block):
    child_nodes = []
    if "*" in block:
        italic_split = re.split(r'(\*.*?(\*|$))', block)
        child_nodes.extend(delimiter_block_helper(italic_split, '*', "italic"))
    if "**" in block:
        bold_split = re.split(r'(\*\*.*?(\*\*|$))', block)
        child_nodes.extend(delimiter_block_helper(bold_split, "**", "bold"))
    if "`" in block:
        code_split = re.split(r'(\`.*?(\`|$))', block)
        child_nodes.extend(delimiter_block_helper(code_split, "`", "code"))
    return child_nodes



def delimiter_block_helper(split_text, delimiter, text_type):
    new_nodes = []
    
    tags = {
        "italic": "em",
        "bold": "strong",
        "code": "code"
    }

    #Calculate the length of delimiter to extract the text inside
    delimiter_len = len(delimiter)

    for part in split_text:
        if part.strip(delimiter).strip() == '':
            continue
        if part.startswith(delimiter) and part.endswith(delimiter):
            tag = tags.get(text_type, text_type)
            new_nodes.append(HTMLNode(tag, part[delimiter_len:-delimiter_len]))
        elif part.startswith(delimiter) and not part.endswith(delimiter):
            raise ValueError("Must have matching delimiters")
        elif not part.startswith(delimiter) and part.endswith(delimiter):
            raise ValueError("Must have matching delimiters")
        else:
            new_nodes.append(HTMLNode("span", part))
    return new_nodes
