import re

from textnode import TextNode

text_type_text='text'
text_type_bold='bold'
text_type_italic='italic'
text_type_code='code'

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if delimiter == '*':
            italic_split = re.split(r'(\*.*?\*)', node.text)
            #print(italic_split)
            for part in italic_split:
                if part.startswith('*') and part.endswith('*'):
                    new_nodes.append(TextNode(part[1:-1], text_type_italic))
                else:
                    new_nodes.append(TextNode(part, text_type_text))
        elif delimiter == "**":
            bold_split = re.split(r'(\*\*.*?\*\*)', node.text)
            #print(italic_split)
            for part in bold_split:
                if part.startswith('**') and part.endswith('**'):
                    new_nodes.append(TextNode(part[2:-2], text_type_bold))
                else:
                    new_nodes.append(TextNode(part, text_type_text))
        elif delimiter == "`":
            code_split = re.split(r'(\`.*?\`)', node.text)
            for part in code_split:
                if part.startswith('`') and part.endswith('`'):
                    new_nodes.append(TextNode(part[1:-1], text_type_code))
                else:
                    new_nodes.append(TextNode(part, text_type_text))
        else:
            new_nodes.append(node)

    print(new_nodes)
    return new_nodes

i_node = TextNode("This  is a text with an *italic block* of writing", text_type_text)
b_node = TextNode("This is **boldyyyy** writing", text_type_text)
c_node = TextNode("This one is for code using `codeeeeee` in the strings", text_type_text)

new_i_node = split_nodes_delimiter([i_node], "*", text_type_italic)
new_b_node = split_nodes_delimiter([b_node], "**", text_type_bold)
new_c_node = split_nodes_delimiter([c_node], "`", text_type_code)