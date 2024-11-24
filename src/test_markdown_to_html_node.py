import unittest

from functional_textnode import *

class TestMarkdownToHtmlNode(unittest.TestCase):
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
    
    def test_code_block_basic(self):
        input = """```
        For animals in zoo: food += 1
        ```"""

        expected_node_type = ["pre"]
        expected_value = "For animals in zoo: food += 1"

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual("pre", pre_child_node.tag)

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

        expected_node_type = ["pre"]
        expected_value = """for people in line:
            spot+=1
        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual("pre", pre_child_node.tag)

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

        expected_node_type = ["pre"]
        expected_value = """# Here we put a comment
        sweet = 0

        for sugar in candy:
            sweet += 1

        # Then some space and another comment


        """

        result = markdown_to_html_node(input)

        self.assertEqual("div", result.tag)

        pre_child_node = result.children[0]
        self.assertEqual("pre", pre_child_node.tag)

        code_child_node = pre_child_node.children[0]
        code_child_content = code_child_node.children[0]

        self.assertEqual("code", code_child_node.tag)
        self.assertEqual("text", code_child_content.tag)
        self.assertEqual(expected_value, code_child_content.value)
        



if __name__ == '__main__':
    unittest.main()