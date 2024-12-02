from textnode import TextNode

def markdown_to_blocks(markdown):
    blocks = []
    # Adding flag to check if currently in a block
    current_block = ""
    in_code_block = False
    current_block_type = None

    lines = markdown.split("\n") # Split the markdown by line
    print(f"Lines: {repr(lines)}")
    for line in lines:
        new_type = get_line_type(line)
        stripped_line = line.strip() # Remove any leading and trailing whitespace
        if stripped_line == "```": # Identify if we're entering or leaving a code block
            # If we're not in a code block, we want to add the line and newline and toggle us into the code block
            if in_code_block == False: 
                current_block += line + "\n"
                # Toggle the flag
                in_code_block = True
                current_block_type = "code" 
            # If we are already in the code block, we just want to add the current line (which is just the final code segment closer ``` here) 
            # and toggle that we're no longer in the block
            else: 
                current_block += line
                in_code_block = False
                current_block_type = None
            # If after those checks we're not in a code block, append all the lines we've added to the current block and reset it
            if not in_code_block:
                blocks.append(current_block)
                current_block = ""
        else: # If the line is anything other than just ```
            if in_code_block == True: # If we're in code block, then we want to add the code to the current code block
                current_block += line + "\n"
            elif stripped_line != "": # If the first statement didn't execute, we're not in a code block
                if new_type != current_block_type:
                    current_block_type = new_type
                    if current_block:
                        blocks.append(current_block.strip())
                        current_block = ""
                    current_block += stripped_line
                else:
                    if current_block:
                        current_block += " " + stripped_line
                    else:
                        current_block += stripped_line

    if current_block:
        blocks.append(current_block.strip())
    return blocks

def is_ordered_list(lines):
    if not lines:
        return False
    for i, line in enumerate(lines, start=1):
        if not line.strip().startswith(f"{i}. "):
            return False
    return True
def is_paragraph_break(line):
    stripped = line.strip()
    return (
        stripped == "" or
        stripped.startswith("#") or 
        stripped.startswith("-") or 
        stripped.startswith("*") or
        stripped.startswith(">") or 
        stripped.startswith("```")
    )
def get_line_type(line):
    stripped = line.strip()
    if stripped == "":
        return 'empty'
    elif stripped.startswith("######"):
        return 'h6'
    elif stripped.startswith("#####"):
        return 'h5'
    elif stripped.startswith("####"):
        return 'h4'
    elif stripped.startswith("###"):
        return 'h3'
    elif stripped.startswith("##"):
        return 'h2'
    elif stripped.startswith("#"):
        return 'h1'
    elif stripped.startswith(("- ", "* ")):
        return "unordered_list"
    elif stripped.startswith("> "):
        return "quote"
    elif stripped.startswith("```"):
        return "code"
    else:
        return "paragraph"
    
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

    

