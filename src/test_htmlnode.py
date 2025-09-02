import unittest

from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag = "a",
            value = "Google",
            props = {"href": "https://www.google.com", "target": "_blank",}
            )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_repr(self):
        node = HTMLNode(
            tag = "div",
            value = "Bruddda",
            children = [],
            props = {"class": "container"}
        )
        expected = "HTMLNode(tag=div, value=Bruddda, children=[], props={'class': 'container'})"
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('Hello World')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World')")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image_with_alt_text(self):
        node = TextNode("A beautiful sunset over the mountains", TextType.IMAGE, "https://example.com/sunset.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "A beautiful sunset over the mountains")
        self.assertEqual(html_node.props["src"], "https://example.com/sunset.jpg")

    def test_image_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")


    def test_leaf_to_html_props(self):
        node = LeafNode(
        tag="a",
        value="OpenAI",
        props={"href": "https://openai.com", "target": "_blank", "rel": "noopener"}
    )
        expected = '<a href="https://openai.com" target="_blank" rel="noopener">OpenAI</a>'

        self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
    
if __name__ == "__main__":
    unittest.main()