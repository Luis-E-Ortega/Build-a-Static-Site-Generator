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

def is_ordered_list(lines):
    if not lines:
        return False
    for i, line in enumerate(lines, start=1):
        if not line.strip().startswith(f"{i}. "):
            return False
    return True

def block_to_block_type(markdown_block):
    lines = markdown_block.split('\n')
    match markdown_block:
        case _ if markdown_block.startswith("```") and markdown_block.endswith("```"):
            return "code"
        case _ if markdown_block.startswith(("# ", '## ', '### ', '#### ', '##### ', '###### ')):
            return 'heading'
        case _ if all(line.strip().startswith("> ") for line in lines):
            return 'quote'
        case _ if all(line.strip().startswith(("* ", "- ")) for line in lines):
            return "unordered_list"
        case _ if is_ordered_list(lines):
            return "ordered_list"
        case _:
            return "paragraph"

    

