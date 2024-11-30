from textnode import TextNode

def markdown_to_blocks(markdown):
    blocks = []
    # Adding flag to check if currently in a block
    current_block = ""
    in_code_block = False

    lines = markdown.split("\n")
    print(f"Lines: {repr(lines)}")
    for line in lines:
        stripped_line = line.strip() # Remove any leading and trailing whitespace
        if stripped_line == "```": # Identify if we're entering or leaving a code block
            # If we're not in a code block, we want to add the line and newline and toggle us into the code block
            if in_code_block == False: 
                current_block += line + "\n"
                # Toggle the flag
                in_code_block = True
            # If we are already in the code block, we just want to add the current line (which is just the final code segment closer ``` here) 
            # and toggle that we're no longer in the block
            else: 
                current_block += line
                in_code_block = False
            # If after those checks we're not in a code block, append all the lines we've added to the current block and reset it
            if not in_code_block:
                blocks.append(current_block)
                current_block = ""
        else: # If the line is anything other than just ```
            if in_code_block == True: # If we're in code block, then we want to add the code to the current code block
                current_block += line + "\n"
            elif in_code_block == False and stripped_line != "": # Conditions to check that it isn't a code related block that needs to be put together unaltered
                current_block += line + "\n"
                if current_block:
                    blocks.append(current_block.strip())
                    current_block = ""
    if current_block: # In case there is anything left over, we want to add it
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

    

