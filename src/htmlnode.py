class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, "
                f"children={self.children}, props={self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None and tag not in ["hr", "br", "img"]:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None and self.tag in ["hr", "br", "img"]:
            props_html = self.props_to_html()
            if props_html:
                props_html = " " + props_html
            return f"<{self.tag}{props_html} />"

        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props_html = self.props_to_html()
        if props_html:
            props_html = " " + props_html
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag.")
        if children is None or len(children) == 0:
            raise ValueError("ParentNode must have children.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have children.")

        props_html = self.props_to_html()
        if props_html:
            props_html = " " + props_html

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
