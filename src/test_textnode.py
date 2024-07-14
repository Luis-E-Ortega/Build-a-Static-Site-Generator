import unittest

from textnode import TextNode, LeafNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_neq_different_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node, node2)
    def test_neq_different_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
    def test_eq_none_url(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)
    def test_neq_one_none_url(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", "http://example.com")
        self.assertNotEqual(node, node2)
    def test_eq_all_properties(self):
        node = TextNode("Sample text", "bold", "http://example.com")
        node2 = TextNode("Sample text", "bold", "http://example.com")
        self.assertEqual(node, node2)
    def test_neq_different_urls(self):
        node = TextNode("Sample text", "bold", "http://example.com")
        node2 = TextNode("Sample text", "bold", "http://anotherexample.com")
        self.assertNotEqual(node, node2)


    #Section for testing TextNode to LeafNode conversions
    def test_basic_text_to_leaf_node(self):
        text_node = TextNode("This is basic text with no tag", "text")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "This is basic text with no tag")
        self.assertEqual(result.props, None)
    def test_bold(self):
        text_node = TextNode("This is bold!", "bold")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "This is bold!")
        self.assertEqual(result.props, None)
    def test_italic(self):
        text_node = TextNode("This is italic!", 'italic')
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "This is italic!")
        self.assertEqual(result.props, None)
    def test_code(self):
        text_node = TextNode("This is code!", "code")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "This is code!")
        self.assertEqual(result.props, None)
    def test_anchor(self):
        text_node = TextNode("This is a link!", "link", url="http://google.com")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, 'a')
        self.assertEqual(result.value, 'This is a link!')
        self.assertEqual(result.props, {'href': text_node.url})
    def test_image(self):
        text_node = TextNode("", "image", url='http://imagecenter.com/image.png', alt_text="An image of a wizard")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, 'img')
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {'src': 'http://imagecenter.com/image.png', 'alt': "An image of a wizard"})
    def test_image_with_none_alt_raises_exception(self):
        text_node = TextNode("", "image", url='http://fantastyquest.com/image.png', alt_text=None)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), 'Missing src or alt in image TextNode')
    def test_image_with_empty_alt_raises_exception(self):
        # Test case for Image Node with empty alt_text
        text_node = TextNode("", "image", url="http://example.com/image.png", alt_text="")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Missing src or alt in image TextNode")
    def test_image_with_none_src_raises_exception(self):
        text_node = TextNode("", "image", url=None, alt_text="A scenic picture of mountains")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Missing src or alt in image TextNode")
    def test_image_with_empty_src_raises_exception(self):
        text_node = TextNode("", "image", url="", alt_text="A scenic picture of mountains")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Missing src or alt in image TextNode")
    def test_not_recognized_text_node_type_raises_exception(self):
        text_node = TextNode("", "The mysterious unknown")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Unknown TextNode type")
    def test_not_recognized_text_node_type_with_image_props_raises_exception(self):
        text_node = TextNode("", "Mystery", url="http://mystery.com", alt_text="A mystery")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Unknown TextNode type")
    def test_none_text_node_type_with_image_props_raises_exception(self):
        text_node = TextNode("", None, url="http://mystery.com", alt_text="A mystery")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Unknown TextNode type")
if __name__ == "__main__":
    unittest.main()
