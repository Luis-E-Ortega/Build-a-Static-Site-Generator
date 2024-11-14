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

    def test_basic_bold_text(self):
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

    def test_basic_code_text(self):
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

    def test_mixed_italic_and_bold_text(self):
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

if __name__ == '__main__':
    unittest.main()