import unittest

from functional_textnode import TextNode, split_nodes_image, split_nodes_link, extract_markdown_converter, extract_markdown_images, extract_markdown_links, text_type_text, text_type_bold, text_type_code, text_type_image, text_type_italic, text_type_link

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_basic_split_link(self):
        input_node = TextNode("This is some sample text with a link [to nexus](https://www.nexusmods.com) for downloading some mods.", text_type_text)
        result = split_nodes_link([input_node])
        self.assertEqual([TextNode('This is some sample text with a link ', text_type_text), TextNode("to nexus", text_type_link, "https://www.nexusmods.com"), TextNode(" for downloading some mods.", text_type_text)], result)
    def test_basic_split_image(self):
        input_node = TextNode("An image testing ground ![rain clouds](https://www.weather.com/cloud_images) to view some cloud pics.", text_type_text)
        result = split_nodes_image([input_node])
        self.assertEqual([TextNode('An image testing ground ', text_type_text), TextNode("rain clouds", text_type_image, "https://www.weather.com/cloud_images"), TextNode(" to view some cloud pics.", text_type_text)], result)
    def test_multiple_images_split_nodes_image(self):
        input_node = TextNode("Here is an image ![hats](hats.jpg) and another image ![shoes](shoes.jpg) what an outfit!", text_type_text)
        result = split_nodes_image([input_node])
        self.assertEqual([
            TextNode("Here is an image ", text_type_text), 
            TextNode("hats", text_type_image, "hats.jpg"), 
            TextNode(" and another image ", text_type_text),
            TextNode("shoes", text_type_image, "shoes.jpg"),
            TextNode(" what an outfit!", text_type_text)
        ], result)
    def test_multiple_links_split_nodes_link(self):
        input_node = TextNode("Fun games to be played [to steam](https://www.steamvalve.com/games) and stories to be read [to library cloud](https://www.librarycloud.com/books) wow!", text_type_text)
        result = split_nodes_link([input_node])
        self.assertEqual([
            TextNode("Fun games to be played ", text_type_text),
            TextNode("to steam", text_type_link, "https://www.steamvalve.com/games"),
            TextNode(" and stories to be read ", text_type_text),
            TextNode("to library cloud", text_type_link, "https://www.librarycloud.com/books"), 
            TextNode(" wow!", text_type_text)
        ], result)
    def test_special_characters_in_link(self):
        input_node = TextNode("Sometimes links can be weird [odd l!nk@$](https://examp&le.com/pa%th/$#^) like this one", text_type_text)
        result = split_nodes_link([input_node])
        self.assertEqual([
            TextNode("Sometimes links can be weird ", text_type_text),
            TextNode("odd l!nk@$", text_type_link, "https://examp&le.com/pa%th/$#^"),
            TextNode(" like this one", text_type_text)
        ], result)
    def test_special_characters_in_image(self):
        input_node = TextNode("Alt text can be strange ![description of !337 h@k$](https://cheatcodes.com/*-+) definitely", text_type_text)
        result = split_nodes_image([input_node])
        self.assertEqual([
            TextNode("Alt text can be strange ", text_type_text),
            TextNode("description of !337 h@k$", text_type_image, "https://cheatcodes.com/*-+"),
            TextNode(" definitely", text_type_text)
        ], result)
    def test_empty_link_text(self):
        input_node = TextNode("This is a link with [](https://example.com) empty text", text_type_text)
        result = split_nodes_link([input_node])
        self.assertEqual([
            TextNode("This is a link with ", text_type_text),
            TextNode("",  text_type_link, "https://example.com"),
            TextNode(" empty text", text_type_text)
        ], result)
    def test_empty_alt_text(self):
        input_node = TextNode("This is an image without alt text, ![](img.jpg) that's not good", text_type_text)
        result = split_nodes_image([input_node])
        self.assertEqual([
            TextNode("This is an image without alt text, ", text_type_text),
            TextNode("", text_type_image, "img.jpg"),
            TextNode(" that's not good", text_type_text)
        ], result)
if __name__ == '__main__':
    unittest.main()   
