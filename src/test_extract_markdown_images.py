import unittest

from functional_textnode import TextNode, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestExtractMarkdownImages(unittest.TestCase):
    def test_basic_extract_markdown_images(self):
        text = "Testing text with an image ![image](https://i.imgur.com/abcdef.png)"
        result = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/abcdef.png")], result)

    def test_basic_extract_markdown_links(self):
        text = "Testing regular link for wallpapers [to wallpaper images](https://www.wallpapers.com) and for youtube [to youtube](https://www.youtube.com/funnyvideos)"
        result = extract_markdown_links(text)
        self.assertListEqual([("to wallpaper images", "https://www.wallpapers.com"), ("to youtube", "https://www.youtube.com/funnyvideos")], result)
    def test_mixed_extract_markdown_links(self):
        text = "Testing mixed links using link extractor [to google](https://www.google.com) and ![image](https://i.imgur.com/random.png)"
        result = extract_markdown_links(text)
        self.assertListEqual([("to google", "https://www.google.com")], result)


    def test_basic_split_nodes_image(self):
        pass

    
if __name__ == '__main__':
    unittest.main()   
