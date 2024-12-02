import unittest

from functional_textnode import *

class TestMarkdownToHtmlNode(unittest.TestCase):
    # Section for testing paragraph blocks
    def test_basic_italic_paragraph(self):
        input = "This is basic *italic* text to test a paragraph."

        # Result expects multiple children representing each markdown part
        expected_node_types = ["text", "em", "text"]
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

        expected_node_types = ["text", "strong", "text", "strong", "text"]
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

        expected_node_types = ["text", "code", "text", "code"]
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

        expected_node_types = ["text", "strong", "text", "em", "text", "code", "text", "strong"]
        expected_values = ["Now a ", "big", " mix of ", "delicate", " characters displayed by ", "b=d.code", " and added ", "boom"]

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        mixed_node = result.children[0]
        self.assertEqual("p", mixed_node.tag)

        for i, child in enumerate(mixed_node.children):
            self.assertEqual(expected_node_types[i], child.tag)
            self.assertEqual(expected_values[i], child.value)
    
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
        self.assertEqual("Introduction", h1_node.value)

        h2_node = result.children[1]
        self.assertEqual("h2", h2_node.tag)
        self.assertEqual("More info", h2_node.value)

        h3_node = result.children[2]
        self.assertEqual("h3", h3_node.tag)
        self.assertEqual("Conclusion", h3_node.value)
    
    def test_basic_heading_with_content(self):
        input = """
        # EXTRA EXTRA, READ ALL ABOUT IT!
        Today in history - passage
        ## Opposing news
        What really happened
        """

        result = markdown_to_html_node(input)
        self.assertEqual("div", result.tag)

        h1_node = result.children[0]
        self.assertEqual("h1", h1_node.tag)
        self.assertEqual("EXTRA EXTRA, READ ALL ABOUT IT!", h1_node.value)

        h1_para_node = result.children[1]
        self.assertEqual("p", h1_para_node.tag)
        self.assertEqual("Today in history - passage", h1_para_node.children[0].value)

        h2_node = result.children[2]
        self.assertEqual("h2", h2_node.tag)
        self.assertEqual("Opposing news", h2_node.value)

        h2_para_node = result.children[3]
        self.assertEqual("p", h2_para_node.tag)
        self.assertEqual("What really happened", h2_para_node.children[0].value)
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
        self.assertEqual("The first rule is important", h1_node.value)

        h1_para = result.children[1]
        self.assertEqual("p", h1_para.tag)

        expected_h1_para_types = ["text", "em", "text", "strong", "text", "strong"]
        expected_h1_para_values = ["Never forget that the ", "first", " rule ", "matters", " it really matters ", "a lot"]

        for i, child in enumerate(h1_para.children):
            self.assertEqual(expected_h1_para_types[i], child.tag)
            self.assertEqual(expected_h1_para_values[i], child.value)
        
        h2_node = result.children[2]
        self.assertEqual("h2", h2_node.tag)
        self.assertEqual("The second rule enriches", h2_node.value)

        h2_para = result.children[3]
        self.assertEqual("p", h2_para.tag)

        expected_h2_para_types = ["text", "strong", "text", "em"]
        expected_h2_para_values = ["How ", "wonderful", " the ", "joy"]

        for i, child in enumerate(h2_para.children):
            self.assertEqual(expected_h2_para_types[i], child.tag)
            self.assertEqual(expected_h2_para_values[i], child.value)

        h3_node = result.children[4]
        self.assertEqual("h3", h3_node.tag)
        self.assertEqual("The third rule confirms", h3_node.value)

        h3_para = result.children[5]
        self.assertEqual("p", h3_para.tag)

        expected_h3_para_types = ["text", "strong", "text", "code"]
        expected_h3_para_values = ["We ", "need", " to code this to make sure it works ", "joy in life += 1"]

        for i, child in enumerate(h3_para.children):
            self.assertEqual(expected_h3_para_types[i], child.tag)
            self.assertEqual(expected_h3_para_values[i], child.value)




if __name__ == '__main__':
    unittest.main()