import unittest
from textnode import *
from blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_markdown_to_blocks(self):
        input_text = "Line one test\nWith stuff\nAnd more stuff \n\n Line 2 and \n\n Line 3"
        result = markdown_to_blocks(input_text)
        self.assertEqual(["Line one test With stuff And more stuff", "Line 2 and", "Line 3"], result)
    def test_empty_markdown_to_blocks(self):
        input_text = ""
        result = markdown_to_blocks(input_text)
        self.assertEqual([], result)
    def test_one_line_markdown_to_blocks(self):
        input_text = "Single line"
        result = markdown_to_blocks(input_text)
        self.assertEqual(["Single line"], result)
    def test_multiple_new_lines_markdown_to_blocks(self):
        input_text = "First line\n\n\n\n\nSecond Line\nSame Block\nStill same block"
        result = markdown_to_blocks(input_text)
        self.assertEqual(["First line", "Second Line Same Block Still same block"], result)
    def test_whitespace_handling(self):
        input_text = "     \t  First block \n\n     Second block\t   \n\nThird block     \n"
        result = markdown_to_blocks(input_text)
        self.assertEqual(["First block", "Second block", "Third block"], result)


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a simple paragraph."
        result = block_to_block_type(block)
        self.assertEqual("paragraph", result)
    def test_heading(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual("heading", result)
    def test_heading_extra(self):
        block = "#### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual("heading", result)
    def test_code(self):
        block = "```Code check```"
        result = block_to_block_type(block)
        self.assertEqual('code', result)
    def test_quote(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual('quote', result)
    def test_unordered_list(self):
        block = "* Item 1\n- Item 2\n* Item 3"
        result = block_to_block_type(block)
        self.assertEqual('unordered_list', result)
    def test_ordered_list(self):
        block = "1. First\n2. 2nd\n3. Three"
        result = block_to_block_type(block)
        self.assertEqual('ordered_list', result)
    def test_multi_line_quote(self):
        block = '> This is a quote, line one\n> That continues\n> And continues'
        result = block_to_block_type(block)
        self.assertEqual('quote', result)
    def test_multi_line_non_quote(self):
        block = '> This is a quote, line one\n>That continues\n>And continues'
        result = block_to_block_type(block)
        self.assertEqual('paragraph', result)
    def test_complex_ordered_list(self):
        block = "1. First\n2. Second\n10. Tenth\n11. Eleventh"
        result = block_to_block_type(block)
        self.assertEqual('ordered_list', result)
    def test_ordered_list_not_starting_with_one(self):
        block = "2. Second\n3. Third\n4. Fourth"
        result = block_to_block_type(block)
        self.assertEqual('ordered_list', result)

if __name__ == '__main__':
    unittest.main()  
