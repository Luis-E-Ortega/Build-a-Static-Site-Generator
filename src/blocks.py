from textnode import TextNode

def markdown_to_blocks(markdown):
    blocks = []
    # Adding flag to check if currently in a block
    current_block = ""
    in_code_block = False

    lines = markdown.split("\n")
    for line in lines:
        if line.strip() == "```":
            if in_code_block == False:
                current_block += line + "\n"
                # Toggle the flag
                in_code_block = not in_code_block
            else:
                current_block += line
                in_code_block = not in_code_block

            if not in_code_block:
                blocks.append(current_block)
                current_block = ""
        else:
            if in_code_block == True:
                current_block += line + "\n"
            else:
                if line.strip() != "":
                    current_block += line + "\n"
                elif current_block:
                    blocks.append(current_block.strip())
                    current_block = ""
    if current_block:
        if in_code_block:
            blocks.append(current_block)
        else:
            blocks.append(current_block.strip())
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
    stripped_block = markdown_block.strip()
    match stripped_block:
        case _ if stripped_block.startswith("```") and stripped_block.endswith("```"):
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

    

