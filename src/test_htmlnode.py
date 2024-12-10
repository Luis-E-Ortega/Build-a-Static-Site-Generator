import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(tag='a', props={' href': 'https://www.google.com', 'target': '_blank'})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')
    def test_props_to_html_with_single_prop(self):
        node = HTMLNode(tag='img', props={' src': 'image.png'})
        result = node.props_to_html()
        self.assertEqual(result, ' src="image.png"')
    def test_props_to_html_with_no_props(self):
        node = HTMLNode(tag='p')
        result = node.props_to_html()
        self.assertEqual(result, "")


class TestLeafNode(unittest.TestCase):

    def test_basic_leaf_node(self):
        leaf = LeafNode("p", "This is a paragraph.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph.</p>")
    def test_no_tag_leaf_node(self):
        leaf_no_tag = LeafNode(None, "This is just a string with no tag.")
        self.assertEqual(leaf_no_tag.to_html(), "This is just a string with no tag.")
    def test_no_value_leaf_node(self):
        with self.assertRaises(ValueError):
            leaf_no_value = LeafNode("p", None)
            leaf_no_value.to_html()
    def test_with_props_leaf_node(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        leaf_with_props = LeafNode("a", "Click me!", props)
        self.assertEqual(leaf_with_props.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')
    def test_without_props_leaf_node(self):
        leaf_without_props = LeafNode("span", "No properties here.", props=None)
        self.assertEqual(leaf_without_props.to_html(), "<span>No properties here.</span>")

class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],

        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_no_tag_parent_node(self):
        node = ParentNode(
            "",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],

        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "No tag was provided.")

    def test_no_children_parent_node(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Children are required for this node.")

    def test_nested_parent_nodes(self):
        node = ParentNode(
        "div",
        [
            LeafNode(None, "Outer text"),
            ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                ],
            ),
            LeafNode("i", "Italic outer text"),
        ],
    )
        self.assertEqual(node.to_html(), "<div>Outer text<p><b>Bold text</b>Normal text</p><i>Italic outer text</i></div>")
    
    def test_sibling_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        LeafNode("h1", "Title 1"),
                        LeafNode(None, "Description 1"),
                    ],
                ),
                ParentNode(
                    "section",
                    [
                        LeafNode("h1", "Title 2"),
                        LeafNode(None, "Description 2"),
                    ],
                ),
            ],
        )
        self.assertEqual(node.to_html(), "<div><section><h1>Title 1</h1>Description 1</section><section><h1>Title 2</h1>Description 2</section></div>")

    def test_single_leaf_node(self):
        node = ParentNode(
            "span",
            [
                LeafNode(None, "Just text"),
            ],
        )
        self.assertEqual(node.to_html(), "<span>Just text</span>")

    def test_children_with_different_tags(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Confirmation letter"),
                LeafNode("p", "This is a letter with words."),
                LeafNode("a", "This is a link in the letter")
            ]
        )
        self.assertEqual(node.to_html(), "<div><h1>Confirmation letter</h1><p>This is a letter with words.</p><a>This is a link in the letter</a></div>")

    def test_empty_string_in_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Text before empty"),
                LeafNode(None, ""),
                LeafNode(None, "Text after empty"),
            ]
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "A value is required for a LeafNode")

    def test_none_value_in_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", None)
            ]
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "A value is required for a LeafNode")
if __name__ == '__main__':
    unittest.main()
