class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
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