import unittest
from textnode import *
from functional_textnode import *

class TestTextToTextnodes(unittest.TestCase):
    def test_basic_text_conversion(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(input_text)
        self.assertEqual([
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ], result)
    def test_blank_text(self):
        input_text = ''
        result = text_to_textnodes(input_text)
        #Our text_to_textnodes function always returns at least one node, even for blank input
        self.assertEqual([TextNode('', text_type_text, None, None)
], result)
    def test_text_to_textnodes(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input_text)
        
        assert len(nodes) == 10
        assert nodes[0] == TextNode("This is ", text_type_text)
        assert nodes[1] == TextNode("text", text_type_bold)
        assert nodes[2] == TextNode(" with an ", text_type_text)
        assert nodes[3] == TextNode("italic", text_type_italic)
        assert nodes[4] == TextNode(" word and a ", text_type_text)
        assert nodes[5] == TextNode("code block", text_type_code)
        assert nodes[6] == TextNode(" and an ", text_type_text)
        assert nodes[7] == TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        assert nodes[8] == TextNode(" and a ", text_type_text)
        assert nodes[9] == TextNode("link", text_type_link, "https://boot.dev")

        print("All assertions passed!")
if __name__ == '__main__':
    unittest.main()   