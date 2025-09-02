class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        parts = []
        for key, value in self.props.items():
            parts.append(f' {key}="{value}"')
        return "".join(parts)
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag")
        if not self.children or self.children is None:
            raise ValueError("missing children")
        else:
            middle = ""
            for child in self.children:
                middle += f"{child.to_html()}"
            start = f"<{self.tag}>"
            end = f"</{self.tag}>"
            final = start + middle + end
            return final

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        else:
            props_string = self.props_to_html() if self.props else ""
            return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"



