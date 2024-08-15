import unittest

from functional_textnode import TextNode, extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_basic_extract_markdown_images(self):
        text = "Testing text with an image ![image](https://i.imgur.com/abcdef.png)"
        result = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/abcdef.png")], result)

    def test_basic_extract_markdown_links(self):
        text = "Testing regular link for wallpapers [to wallpaper images](https://www.wallpapers.com) and for youtube [to youtube](https://www.youtube.com/funnyvideos)"
        result = extract_markdown_links(text)
        self.assertListEqual([("to wallpaper images", "https://www.wallpapers.com"), ("to youtube", "https://www.youtube.com/funnyvideos")], result)
    
if __name__ == '__main__':
    unittest.main()   
