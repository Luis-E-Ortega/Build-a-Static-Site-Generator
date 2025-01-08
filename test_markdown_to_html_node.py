import unittest

from functional_textnode import *

class TestMarkdownToHtmlNode(unittest.TestCase):
    # Section for testing paragraph blocks
    def test_basic_italic_paragraph(self):
        input = "This is basic *italic* text to test a paragraph."

        # Result expects multiple children representing each markdown part
        expected_node_types = [None, "i", None]
        expected_values = ["This is basic ", "italic", " text to test a paragraph."]

        # Convert the markdown input to HTML node
        result = markdown_to_html_node(input)

        # Verify the root node's tag
        self.assertEqual("div", result.tag)

        # Verify the paragraph node
        paragraph_node = result.children[0]
        self.assertEqual("p", paragraph_node.tag)

        # Verify the children of the paragraph node
        self.assertEqual(len(expected_node_types), len(paragraph_node.children))

        # Check each expected node type and value
        for i, child in enumerate(paragraph_node.children):
            self.assertEqual(expected_node_types[i], child.tag)
            self.assertEqual(expected_values[i], child.value)

    def test_basic_bold_paragraph_text(self):
        input = "Testing just **bold** text for this **intense** part"

        expected_node_types = [None, "b", None, "b", None]
        expected_values = ["Testing just ", "bold", " text for this ", "intense", " part"]

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        paragraph_node = result.children[0]
        self.assertEqual("p", paragraph_node.tag)

        self.assertEqual(len(expected_node_types), len(paragraph_node.children))

        for i, child in enumerate(paragraph_node.children):
            self.assertEqual(expected_node_types[i], child.tag)
            self.assertEqual(expected_values[i], child.value)

    def test_basic_code_paragraph_text(self):
        input = "Here we have some `code` testing that involves more code like `parts.blob+=2`"

        expected_node_types = [None, "code", None, "code"]
        expected_values = ["Here we have some ", "code", " testing that involves more code like ", "parts.blob+=2"]

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        paragraph_node = result.children[0]
        self.assertEqual("p", paragraph_node.tag)

        self.assertEqual(len(expected_node_types), len(paragraph_node.children))

        for i, child in enumerate(paragraph_node.children):
            self.assertEqual(expected_node_types[i], child.tag)
            self.assertEqual(expected_values[i], child.value)

    def test_mixed_italic_bold_and_code_paragraph_text(self):
        input = "Now a **big** mix of *delicate* characters displayed by `b=d.code` and added **boom**"

        expected_node_types = [None, "b", None, "i", None, "code", None, "b"]
        expected_values = ["Now a ", "big", " mix of ", "delicate", " characters displayed by ", "b=d.code", " and added ", "boom"]

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        mixed_node = result.children[0]
        self.assertEqual("p", mixed_node.tag)

        for i, child in enumerate(mixed_node.children):
            self.assertEqual(expected_node_types[i], child.tag)
            self.assertEqual(expected_values[i], child.value)
    def test_multi_line_basic_paragraph(self):
        input = """
        Begin testing of paragraph
        with multiple lines
        and extra content
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        p_node = result.children[0]
        self.assertEqual("p", p_node.tag)
        self.assertEqual("Begin testing of paragraph with multiple lines and extra content", p_node.children[0].value)
    def test_multi_basic_paragraph(self):
        input = """
        In paragraph one we introduce

        Then in paragraph two we expand

        Finally in paragraph three we complete
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        p1_node = result.children[0]
        self.assertEqual("p", p1_node.tag)
        self.assertEqual("In paragraph one we introduce", p1_node.children[0].value)

        p2_node = result.children[1]
        self.assertEqual("p", p2_node.tag)
        self.assertEqual("Then in paragraph two we expand", p2_node.children[0].value)

        p3_node = result.children[2]
        self.assertEqual("p", p3_node.tag)
        self.assertEqual("Finally in paragraph three we complete", p3_node.children[0].value)
    
    # Section for testing code blocks
    def test_code_block_basic(self):
        input = """```
        For animals in zoo: food += 1
        ```"""

        expected_node_type = "pre"
        expected_value = "For animals in zoo: food += 1"

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual(expected_node_type, pre_child_node.tag)

        code_child_node = pre_child_node.children[0]
        code_child_content = code_child_node.children[0]
        self.assertEqual("code", code_child_node.tag)
        self.assertEqual("text", code_child_content.tag)
        self.assertEqual(expected_value, code_child_content.value)

    def test_code_block_multiple_lines(self):
        input = """```
        for people in line:
            spot+=1
        ```"""

        expected_node_type = "pre"
        expected_value = """for people in line:
            spot+=1
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual(expected_node_type, pre_child_node.tag)

        code_child_node = pre_child_node.children[0]
        code_child_content = code_child_node.children[0]
        self.assertEqual("code", code_child_node.tag)
        self.assertEqual("text", code_child_content.tag)
        self.assertEqual(expected_value, code_child_content.value)

    def test_code_with_empty_lines(self):
        input = """```
        # Here we put a comment
        sweet = 0

        for sugar in candy:
            sweet += 1

        # Then some space and another comment
        
        
        
        
        ```"""

        expected_node_type = "pre"
        expected_value = """# Here we put a comment
        sweet = 0

        for sugar in candy:
            sweet += 1

        # Then some space and another comment
        
        
        
        
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual(expected_node_type, pre_child_node.tag)

        code_child_node = pre_child_node.children[0]
        code_child_content = code_child_node.children[0]

        self.assertEqual("code", code_child_node.tag)
        self.assertEqual("text", code_child_content.tag)
        self.assertEqual(expected_value, code_child_content.value)
    
    def test_empty_code_block(self):
        input = """```
        
        ```"""

        expected_node_type = "pre"
        expected_value = ""

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual(expected_node_type, pre_child_node.tag)

        code_child_node = pre_child_node.children[0]
        code_child_content = code_child_node.children[0]

        self.assertEqual("code", code_child_node.tag)
        self.assertEqual("text", code_child_content.tag)
        self.assertEqual(expected_value, code_child_content.value)

    # Section for testing heading blocks
    def test_basic_multi_level_heading(self):
        input = """
        # Introduction
        ## More info
        ### Conclusion
        """

        result = markdown_to_html_node(input)
        self.assertEqual("div", result.tag)

        h1_node = result.children[0]
        self.assertEqual("h1", h1_node.tag)
        h1_text_node = h1_node.children[0]
        #self.assertEqual("text", h1_text_node.tag)
        self.assertEqual("Introduction", h1_text_node.value)

        h2_node = result.children[1]
        self.assertEqual("h2", h2_node.tag)
        h2_text_node = h2_node.children[0]
        #self.assertEqual("text", h2_text_node.tag)
        self.assertEqual("More info", h2_text_node.value)

        h3_node = result.children[2]
        self.assertEqual("h3", h3_node.tag)
        h3_text_node = h3_node.children[0]
        #self.assertEqual("text", h3_text_node.tag)
        self.assertEqual("Conclusion", h3_text_node.value)
    
    def test_basic_heading_with_content(self):
        input = """
        # EXTRA EXTRA, READ ALL ABOUT IT!
        Today in history - passage
        ## Opposing news
        What really happened
        """

        result = markdown_to_html_node(input)
        self.assertEqual("div", result.tag)

        # First heading (h1)
        h1_node = result.children[0]
        self.assertEqual("h1", h1_node.tag)
        h1_text_node = h1_node.children[0]
        #self.assertEqual("text", h1_text_node.tag)
        self.assertEqual("EXTRA EXTRA, READ ALL ABOUT IT!", h1_text_node.value)

        # First paragraph
        h1_para_node = result.children[1]
        self.assertEqual("p", h1_para_node.tag)
        para1_text_node = h1_para_node.children[0]
        #self.assertEqual("text", para1_text_node.tag)
        self.assertEqual("Today in history - passage", para1_text_node.value)

        # Second heading (h2)
        h2_node = result.children[2]
        self.assertEqual("h2", h2_node.tag)
        h2_text_node = h2_node.children[0]
        #self.assertEqual("text", h2_text_node.tag)
        self.assertEqual("Opposing news", h2_text_node.value)

        # Second paragraph
        h2_para_node = result.children[3]
        self.assertEqual("p", h2_para_node.tag)
        para2_text_node = h2_para_node.children[0]
        self.assertEqual("What really happened", para2_text_node.value)
    def test_complex_heading_with_content(self):
        input = """
        # The first rule is important
        Never forget that the *first* rule **matters**
        it really matters **a lot**
        ## The second rule enriches
        How **wonderful** the *joy*
        ### The third rule confirms
        We **need** to code this to make sure it works `joy in life += 1`
        """

        result = markdown_to_html_node(input)
        self.assertEqual("div", result.tag)

        h1_node = result.children[0]
        self.assertEqual("h1", h1_node.tag)
        h1_text_node = h1_node.children[0]
        #self.assertEqual("text", h1_text_node.tag)
        self.assertEqual("The first rule is important", h1_text_node.value)

        h1_para = result.children[1]
        self.assertEqual("p", h1_para.tag)

        expected_h1_para_types = [None, "i", None, "b", None, "b"]
        expected_h1_para_values = ["Never forget that the ", "first", " rule ", "matters", " it really matters ", "a lot"]

        for i, child in enumerate(h1_para.children):
            self.assertEqual(expected_h1_para_types[i], child.tag)
            self.assertEqual(expected_h1_para_values[i], child.value)
        
        h2_node = result.children[2]
        self.assertEqual("h2", h2_node.tag)
        h2_text_node = h2_node.children[0]
        #self.assertEqual("text", h2_text_node.tag)
        self.assertEqual("The second rule enriches", h2_text_node.value)

        h2_para = result.children[3]
        self.assertEqual("p", h2_para.tag)

        expected_h2_para_types = [None, "b", None, "i"]
        expected_h2_para_values = ["How ", "wonderful", " the ", "joy"]

        for i, child in enumerate(h2_para.children):
            self.assertEqual(expected_h2_para_types[i], child.tag)
            self.assertEqual(expected_h2_para_values[i], child.value)

        h3_node = result.children[4]
        self.assertEqual("h3", h3_node.tag)
        h3_text_node = h3_node.children[0]
        #self.assertEqual("text", h3_text_node.tag)
        self.assertEqual("The third rule confirms", h3_text_node.value)

        h3_para = result.children[5]
        self.assertEqual("p", h3_para.tag)

        expected_h3_para_types = [None, "b", None, "code"]
        expected_h3_para_values = ["We ", "need", " to code this to make sure it works ", "joy in life += 1"]

        for i, child in enumerate(h3_para.children):
            self.assertEqual(expected_h3_para_types[i], child.tag)
            self.assertEqual(expected_h3_para_values[i], child.value)

    # Section for testing quotes     
    def test_basic_quote(self):
        input = """
        > This is a basic quote
        """
        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        quote_node = result.children[0]
        self.assertEqual("blockquote", quote_node.tag)

        p_node = quote_node.children[0]
        self.assertEqual(None, p_node.tag)

        self.assertEqual("This is a basic quote", p_node.value)
    def test_multi_line_basic_quote(self):
        input = """
        > The music was great and
        > it filled the air with energy
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        quote_node = result.children[0]
        self.assertEqual("blockquote", quote_node.tag)

        p_node = quote_node.children[0]
        self.assertEqual(None, p_node.tag)

        self.assertEqual("The music was great and it filled the air with energy", p_node.value)
    def test_multiple_quotes_basic(self):
        input = """
        > The day was sunny but
        > also very hot.

        > How nice it would be
        > if it were just a bit cooler.
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        # First quote
        q1_node = result.children[0]
        self.assertEqual("blockquote", q1_node.tag)
        q1_p_node = q1_node.children[0]
        self.assertEqual(None, q1_p_node.tag)
        self.assertEqual("The day was sunny but also very hot.", q1_p_node.value)

        # Second quote
        q2_node = result.children[1]
        self.assertEqual("blockquote", q2_node.tag)
        q2_p_node = q2_node.children[0]
        self.assertEqual(None, q2_p_node.tag)
        self.assertEqual("How nice it would be if it were just a bit cooler.", q2_p_node.value)
    def test_basic_quote_and_paragraph_mix(self):
        input = """
        > The arena was bustling

        The number of people was too high to count

        > It made everyone realize how popular the band had become
        
        In enters the band and begins playing
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        # First quote
        q1_node = result.children[0]
        self.assertEqual("blockquote", q1_node.tag)
        q1_p_node = q1_node.children[0]
        self.assertEqual(None, q1_p_node.tag)
        self.assertEqual("The arena was bustling", q1_p_node.value)

        # First paragraph
        p1_node = result.children[1]
        self.assertEqual("p", p1_node.tag)
        p1_text_node = p1_node.children[0]
        self.assertEqual(None, p1_text_node.tag)
        self.assertEqual("The number of people was too high to count", p1_text_node.value)

        # Second quote
        q2_node = result.children[2]
        self.assertEqual("blockquote", q2_node.tag)
        q2_p_node = q2_node.children[0]
        self.assertEqual(None, q2_p_node.tag)
        self.assertEqual("It made everyone realize how popular the band had become", q2_p_node.value)

        # Second paragraph
        p2_node = result.children[3]
        self.assertEqual("p", p2_node.tag)
        p2_text_node = p2_node.children[0]
        self.assertEqual(None, p2_text_node.tag)
        self.assertEqual("In enters the band and begins playing", p2_text_node.value)
        
    # Section for testing unordered lists
    def test_basic_unordered_list(self):
        input = """
        * Fire
        * Frost
        * Shadow
        * Mist
        """

        result = markdown_to_html_node(input.strip())

        self.assertEqual("div", result.tag)

        ul_node = result.children[0]
        #print("UL node children count:", len(ul_node.children))  # Debug print
        self.assertEqual("ul", ul_node.tag)

        expected_texts = ["Fire", "Frost", "Shadow", "Mist"]

        for i, expected_text in enumerate(expected_texts):
            with self.subTest(i=i):
                li_node = ul_node.children[i]
                self.assertEqual("li", li_node.tag)

                print("LI node found:", li_node.tag)  # Debug print
                text_nodes = li_node.children[0]
                text_value = text_nodes.value
                print("Text node value:", text_nodes.value)  # Debug print
                
                self.assertEqual(expected_text, text_value)
    def test_basic_multi_unordered_list(self):
        input = """
        - Earth
        - Water

        - Darkness
        - Light
        """

        result = markdown_to_html_node(input.strip())

        self.assertEqual("div", result.tag)

        ul1_node = result.children[0]
        self.assertEqual("ul", ul1_node.tag)
        expected_texts = ["Earth", "Water"]

        for i, expected_text in enumerate(expected_texts):
            with self.subTest(i=i):
                li_node = ul1_node.children[i]
                text_node = li_node.children[0]
                self.assertEqual(expected_text, text_node.value)
        
        ul2_node = result.children[1]
        self.assertEqual("ul", ul2_node.tag)
        expected_texts_2 = ["Darkness", "Light"]

        for i, expected_text in enumerate(expected_texts_2):
            with self.subTest(i=i):
                li_node = ul2_node.children[i]
                text_node = li_node.children[0]
                self.assertEqual(expected_text, text_node.value)
    def test_complex_single_list(self):
        input = """
        * The warrior **slams**
        * The fighter *dodges*
        * The mage teleports with code `teleport = True`
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        ul_node = result.children[0]
        self.assertEqual("ul", ul_node.tag)

        expected_texts = [
            ["The warrior ", "slams"],
            ["The fighter ", "dodges"],
            ["The mage teleports with code ", "teleport = True"]
        ]
        expected_tags = [
            ["text", "strong"],
            ["text", "em"],
            ["text", "code"]
        ]

        for i, (expected_text_parts, expected_tag_parts) in enumerate(zip(expected_texts, expected_tags)):
            with self.subTest(i=i):
                li_node = ul_node.children[i]
                #print("Children in list: ", len(li_node.children))  # Check how many children each list item has
                #print("How many children expected: ", len(expected_text_parts))  # What you're expecting
                for j, (expected_text, expected_tag) in enumerate(zip(expected_text_parts, expected_tag_parts)):
                    child_node = li_node.children[j]
                    #self.assertEqual(expected_tag, child_node.tag)
                    self.assertEqual(expected_text, child_node.value)
    def test_complex_multi_inline_single_list(self):
        input = """
        * The bard *sings* songs of **power**
        * The witch curses `curse_spread *= num_enemies` and *hexes* every **giant** around
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        ul_node = result.children[0]
        self.assertEqual("ul", ul_node.tag)

        expected_texts = [
            ["The bard ", "sings", " songs of ", "power"], 
            ["The witch curses ", "curse_spread *= num_enemies", " and ", "hexes", " every ", "giant", " around"]
        ]
        expected_tags = [
            [None, "i", None, "b"], 
            [None, "code", None, "i", None, "b", None]
        ]

        for i, (expected_text_parts, expected_tag_parts) in enumerate(zip(expected_texts, expected_tags)):
            with self.subTest(i=i):
                li_node = ul_node.children[i]
                for j, (expected_text, expected_tag) in enumerate(zip(expected_text_parts, expected_tag_parts)):
                    child_node = li_node.children[j]
                    self.assertEqual(expected_tag, child_node.tag)
                    self.assertEqual(expected_text, child_node.value)
    def test_complex_inline_and_multi_list(self):
        input = """
        * The warrior **slams**
        * The fighter *dodges*
        * The mage teleports with code `teleport = True`

        * The bard *sings* songs of **power**
        * The witch curses `curse_spread *= num_enemies` and *hexes* every **giant** around        
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        ul1_node = result.children[0]
        self.assertEqual("ul", ul1_node.tag)

        expected_texts = [
            ["The warrior ", "slams"],
            ["The fighter ", "dodges"],
            ["The mage teleports with code ", "teleport = True"]
        ]
        expected_tags = [
            [None, "b"],
            [None, "i"],
            [None, "code"]
        ]

        for i, (expected_text_parts, expected_tag_parts) in enumerate(zip(expected_texts, expected_tags)):
            with self.subTest(i=i):
                li_node = ul1_node.children[i]
                #print("Children in list: ", len(li_node.children))  # Check how many children each list item has
                #print("How many children expected: ", len(expected_text_parts))  # What you're expecting
                for j, (expected_text, expected_tag) in enumerate(zip(expected_text_parts, expected_tag_parts)):
                    child_node = li_node.children[j]
                    self.assertEqual(expected_tag, child_node.tag)
                    self.assertEqual(expected_text, child_node.value)

        ul2_node = result.children[1]
        self.assertEqual("ul", ul2_node.tag)

        expected_texts = [
            ["The bard ", "sings", " songs of ", "power"], 
            ["The witch curses ", "curse_spread *= num_enemies", " and ", "hexes", " every ", "giant", " around"]
        ]
        expected_tags = [
            [None, "i", None, "b"], 
            [None, "code", None, "i", None, "b", None]
        ]

        for i, (expected_text_parts, expected_tag_parts) in enumerate(zip(expected_texts, expected_tags)):
            with self.subTest(i=i):
                li_node = ul2_node.children[i]
                self.assertEqual("li", li_node.tag)
                for j, (expected_text, expected_tag) in enumerate(zip(expected_text_parts, expected_tag_parts)):
                    child_node = li_node.children[j]
                    self.assertEqual(expected_tag, child_node.tag)
                    self.assertEqual(expected_text, child_node.value)

    # Section for testing ordered_lists
    def test_basic_ordered_list(self):
        input = """
        1. First
        2. Second
        3. Third
        20. Twentieth
        """

        result = markdown_to_html_node(input)
        self.assertEqual("div", result.tag)

        ol_node = result.children[0]
        self.assertEqual("ol", ol_node.tag)

        expected_texts = ["First", "Second", "Third", "Twentieth"]
        expected_tags = ["text", "text", "text", "text"]

        for i, (expected_text, expected_tag) in enumerate(zip(expected_texts, expected_tags)):
            with self.subTest(i=i):
                li_node = ol_node.children[i]
                self.assertEqual("li", li_node.tag)
                text_node = li_node.children[0]
                self.assertEqual(expected_text, text_node.value)
    def test_complex_ordered_list(self):
        input = """
        25. **Powerful** number laughs at *smol* number
        1. *Tiny* number
        12354. Complex numbers rejoice `complex = True` for all to see

        5005. New block number is *sleek*
        400. This number is not as **powerful**
        """

        result = markdown_to_html_node(input)
        self.assertEqual("div", result.tag)

        ol1_node = result.children[0]
        self.assertEqual("ol", ol1_node.tag)

        ol2_node = result.children[1]
        self.assertEqual("ol", ol2_node.tag)

        expected_texts_1 = [
            ["Powerful", " number laughs at ", "smol", " number"],
            ["Tiny", " number"],
            ["Complex numbers rejoice ", "complex = True", " for all to see"]
        ]
        expected_tags_1 = [
            ["b", None, "i", None],
            ["i", None],
            [None, "code", None]
        ]

        for i, (expected_text_parts, expected_tag_parts) in enumerate(zip(expected_texts_1, expected_tags_1)):
            with self.subTest(i=i):
                li_node = ol1_node.children[i]
                self.assertEqual("li", li_node.tag)
                for j, (expected_text, expected_tag) in enumerate(zip(expected_text_parts, expected_tag_parts)):
                    child_node = li_node.children[j]
                    self.assertEqual(expected_tag, child_node.tag)
                    self.assertEqual(expected_text, child_node.value)

        expected_texts_2 = [
            ["New block number is ", "sleek"],
            ["This number is not as ", "powerful"]
        ]
        expected_tags_2 = [
            [None, "i"],
            [None, "b"]
        ]

        for i, (expected_text_parts, expected_tag_parts) in enumerate(zip(expected_texts_2, expected_tags_2)):
            with self.subTest(i=i):
                li_node = ol2_node.children[i]
                self.assertEqual("li", li_node.tag)
                for j, (expected_text, expected_tag) in enumerate(zip(expected_text_parts, expected_tag_parts)):
                    child_node = li_node.children[j]
                    self.assertEqual(expected_tag, child_node.tag)
                    self.assertEqual(expected_text, child_node.value)


if __name__ == '__main__':
    unittest.main()