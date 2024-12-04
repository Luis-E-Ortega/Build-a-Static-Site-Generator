from textnode import TextNode

def markdown_to_blocks(markdown):
    blocks = []
    # Adding flag to check if currently in a block
    current_block = ""
    in_code_block = False
    in_quote_block = False
    in_ul_block = False
    current_block_type = None

    #print(f"Markdown: {repr(markdown)}")
    lines = markdown.split("\n") # Split the markdown by line
    #print(f"Lines: {repr(lines)}")

    for line in lines:
        new_type = get_line_type(line)
        stripped_line = line.strip() # Remove any leading and trailing whitespace

        if stripped_line == "```": # Identify if we're entering or leaving a code block
            # If we're not in a code block, we want to add the line and newline and toggle us into the code block
            if not in_code_block: 
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
        elif stripped_line.startswith(">"): # Identify if we're entering or continuing a blockquote
            # If we're not in a blockquote, we want to add the line without a newline and toggle us into the blockquote
            if not in_quote_block:
                current_block += line
                in_quote_block = True
                current_block_type = "quote"
            # If we are already in the blockquote, we want to strip the leading > and just add the space to continue the quote
            else:
                stripped_quote = stripped_line[1:].lstrip()
                current_block += " " + stripped_quote
        else: # If the line is anything other than just ``` or starting with >
            if in_code_block == True: # If we're in code block, then we want to add the code to the current code block
                current_block += line + "\n"
            elif in_quote_block == True and stripped_line == "": # If we're in a blockquote and encounter anything that doesn't start with >, we toggle off since we're exiting it
                in_quote_block = False 
                blocks.append(current_block.strip())
                current_block = ""
            elif stripped_line == "":
                if current_block:
                    blocks.append(current_block.strip())
                    current_block = ""
                    in_quote_block = False
                    current_block_type = None
                continue
            elif stripped_line != "": # If the first statement didn't execute, we're not in a code block
                if new_type != current_block_type:
                    current_block_type = new_type
                    if current_block:
                        blocks.append(current_block.strip())
                        current_block = ""
                    if current_block_type == "paragraph": # If working with a paragraph, we don't want to insert a new line so it can flow as expected with just a space
                        current_block += stripped_line
                    else: # Everything else wants to add a new line to the current block
                        current_block += stripped_line + "\n"
                else:
                    if current_block: 
                        if current_block_type == "unordered_list": # Unordered lists need a new line rather than just a space for processing
                            current_block += stripped_line + "\n"
                        else:
                            current_block += " " + stripped_line
                    else:
                        current_block += stripped_line 

    if current_block:
        blocks.append(current_block.strip())
    print(f"Blocks: {repr(blocks)}")
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

    

