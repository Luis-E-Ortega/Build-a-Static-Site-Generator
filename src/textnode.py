from htmlnode import LeafNode

class TextNode:
	def __init__(self, text, text_type, url=None, alt_text=None):
		self.text = text
		self.text_type = text_type
		self.url = url
		self.alt_text = alt_text

	def __eq__(self, other):
		return (self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url and
			self.alt_text == other.alt_text)
	
	def __repr__(self):
		return f'TextNode({self.text}, {self.text_type}, {self.url}, {self.alt_text})'
	
def text_node_to_html_node(text_node):
	#print(f"Converting TextNode with text_type: {text_node.text_type}")
	match text_node.text_type:
		case 'text':
			leaf_node = LeafNode(None, text_node.text)
		case 'bold':
			leaf_node = LeafNode("b", text_node.text)
		case 'italic':
			leaf_node = LeafNode("i", text_node.text)
		case 'code':
			leaf_node = LeafNode("code", text_node.text)
		case 'link':
			if text_node.url:
				leaf_node = LeafNode("a", text_node.text, props={'href': text_node.url})
			else:
				raise Exception("Missing href in link TextNode")
		case 'image':
			if text_node.url and text_node.alt_text:
				leaf_node = LeafNode("img", "", props={'src': text_node.url, 'alt': text_node.alt_text})
			else:
				raise Exception("Missing src or alt in image TextNode")
		case _:
			raise Exception("Unknown TextNode type")
	return leaf_node