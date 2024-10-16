from textnode import TextNode

def markdown_to_blocks(markdown):
    blocks = []
    pre_strings = ""
    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.strip() != "":
            pre_strings += line + "\n"
        elif pre_strings:
            blocks.append(pre_strings.strip())
            pre_strings = ""
    if pre_strings:
        blocks.append(pre_strings.strip())
    return blocks

    

