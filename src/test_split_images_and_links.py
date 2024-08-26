import unittest

from functional_textnode import TextNode, split_nodes_image, split_nodes_link, extract_markdown_converter, extract_markdown_images, extract_markdown_links, text_type_text, text_type_bold, text_type_code, text_type_image, text_type_italic, text_type_link

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_basic_split_link(self):
        input_node = TextNode("This is some sample text with a link [to nexus](https://www.nexusmods.com) for downloading some mods.", text_type_text)
        result = split_nodes_link([input_node])
        self.assertEqual([TextNode('This is some sample text with a link ', text_type_text), TextNode("to nexus", text_type_link, "https://www.nexusmods.com"), TextNode(" for downloading some mods.", text_type_text)], result)


if __name__ == '__main__':
    unittest.main()   
