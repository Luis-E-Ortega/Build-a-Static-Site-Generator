import unittest
from textnode import *
from blocks_textnode import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_markdown_to_blocks(self):
        input_text = "Line one test\nWith stuff\nAnd more stuff \n\n Line 2 and \n\n Line 3"
        result = markdown_to_blocks(input_text)
        self.assertEqual(["Line one test\nWith stuff\nAnd more stuff", "Line 2 and", "Line 3"], result)
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
        self.assertEqual(["First line", "Second Line\nSame Block\nStill same block"], result)
    def test_whitespace_handling(self):
        input_text = "     \t  First block \n\n     Second block\t   \n\nThird block     \n"
        result = markdown_to_blocks(input_text)
        self.assertEqual(["First block", "Second block", "Third block"], result)
if __name__ == '__main__':
    unittest.main()  
