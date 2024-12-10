import unittest

from functional_textnode import TextNode, split_nodes_delimiter, delimiter_helper

class TestSplitNodesDelimiter(unittest.TestCase):

    #Section for testing proper delimiter usage for functional textnode
    def test_basic_split_nodes_delimiter_italic(self):
        input_node = TextNode("This is *italic* text", 'text')
        expected_output = [
            TextNode("This is ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" text", 'text')
        ]

        result = split_nodes_delimiter([input_node], "*", 'italic')
        self.assertEqual(result, expected_output)
    def test_basic_split_nodes_delimiter_bold(self):
        input_node = TextNode("This is **bold** text", 'text')
        expected_output = [
            TextNode("This is ", 'text'),
            TextNode("bold", 'bold'),
            TextNode(" text", 'text')
        ]

        result = split_nodes_delimiter([input_node], "**", 'bold')
        self.assertEqual(result, expected_output)
    def test_basic_split_nodes_delimiter_code(self):
        input_node = TextNode("This is `code` text", 'text')
        expected_output = [
            TextNode("This is ", 'text'),
            TextNode("code", 'code'),
            TextNode(" text", 'text')
        ]

        result = split_nodes_delimiter([input_node], "`", 'code')
        self.assertEqual(result, expected_output)
    
    def test_multiple_delimiters_split_nodes_delimiter_bold(self):
        input_node = TextNode("This **is** extra **bolded** text", 'text')
        expected_output = [
            TextNode("This ", 'text'),
            TextNode("is", 'bold'),
            TextNode(" extra ", 'text'),
            TextNode("bolded", 'bold'),
            TextNode(" text", 'text')
        ]

        result = split_nodes_delimiter([input_node], '**', 'bold')
        self.assertEqual(result, expected_output)

    def test_no_delimiter_split_nodes_delimiter(self):
        input_node = TextNode("This is regular plan text", 'text')
        expected_output = [
            TextNode("This is regular plain text", 'text')
        ]
    def test_only_delimiter_split_nodes_delimiter(self):
        input_node = TextNode("****", 'text')
        expected_output = TextNode("", 'text')
    def test_mismatching_bold_start_delimiters_split_nodes_delimiter(self):
        input_node = TextNode("This is `bold** text", 'text')
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input_node], "**", 'bold')
    def test_mismatching_bold_end_delimiters_split_nodes_delimiter(self):
        input_node = TextNode("This is **bold* text", 'text')
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input_node], "**", 'bold')
    def test_mismatching_italic_start_delimiters_split_nodes_delimiter(self):
        input_node = TextNode("This is `italic* text", 'text')
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input_node], "*", 'italic')
    def test_mismatching_italic_end_delimiters_split_nodes_delimiter(self):
        input_node = TextNode("This is *italic** text", 'text')
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input_node], '*', 'italic')
    def test_mismatching_code_delimiters_split_nodes_delimiter(self):
        input_node = TextNode("This is `code**", 'text')
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input_node], "`", 'code')
        

if __name__ == '__main__':
    unittest.main()