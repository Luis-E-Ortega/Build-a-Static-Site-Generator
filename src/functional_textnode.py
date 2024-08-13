import re

from textnode import TextNode

#Create identifiers for each type of delimiter
text_type_text='text'
text_type_bold='bold'
text_type_italic='italic'
text_type_code='code'

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #Empty list to store split nodes into
    new_nodes = []

    '''for node in old_nodes:
        if node.text_type != 'text':
            new_nodes.append(node)
            continue

        text = node.text
        temp_str = ''
        inside_delimiter = False
        i = 0
        delimiter_len = len(delimiter)

        while i < len(text):
            if text[i:i+delimiter_len] == delimiter:
                if inside_delimiter:
                    #Closing delimiter
                    new_nodes.append(TextNode(temp_str, text_type))
                    temp_str = ""
                    inside_delimiter = False
                    i += delimiter_len - 1
                else:
                    #Opening delimiter
                    if temp_str:
                        new_nodes.append(TextNode(temp_str, 'text'))
                    temp_str = ""
                    inside_delimiter = True
                    i += delimiter_len - 1
            else:
                temp_str += text[i]
            i += 1

            #Append any remaining text
            if temp_str:
                if inside_delimiter:
                    raise ValueError("Must have matching delimiters")
                else:
                    new_nodes.append(TextNode(temp_str, 'text'))'''

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

i_node = TextNode("This  is a text with an *italic block* of writing", text_type_text)
b_node = TextNode("This is **boldyyyy** writing", text_type_text)
c_node = TextNode("This one is for code using `codeeeeee` in the strings", text_type_text)

new_i_node = split_nodes_delimiter([i_node], "*", text_type_italic)
new_b_node = split_nodes_delimiter([b_node], "**", text_type_bold)
new_c_node = split_nodes_delimiter([c_node], "`", text_type_code)