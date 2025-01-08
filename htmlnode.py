class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        if any(isinstance(child, str) for child in self.children):
            print(f"Warning: String child found in HTMLNode constructor for tag: {tag}")
        self.props = props
    def to_html(self):
        if not self.tag:
            return self.value if self.value else ""
        
        props_str = self.props_to_html()
        opening_tag = f"<{self.tag}{' ' + props_str if props_str else ''}>"
        closing_tag = f"</{self.tag}>"
        
        if self.children:
            # Parent node behavior
            content = ""
            for i, child in enumerate(self.children):
                if isinstance(child, str):
                    raise ValueError(f"Child {i} of node with tag '{self.tag}' is a string '{child}'. Expected HTMLNode object.")
                content += child.to_html()
            return opening_tag + content + closing_tag
        else:
            # Leaf node behavior
            if self.value is None:
                self.value = ""
            return opening_tag + self.value + closing_tag
    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    def to_html(self):
        if not self.value:
            raise ValueError('A value is required for a LeafNode')
        if not self.tag:
            return self.value

        props_str = self.props_to_html()
        if props_str:
            html_string = f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        else:
            html_string = f"<{self.tag}>{self.value}</{self.tag}>"

        return html_string

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError('No tag was provided.')
        if not self.children:
            raise ValueError('Children are required for this node.')
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html