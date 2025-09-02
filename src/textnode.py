from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url 

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html(self):
        node = text_node_to_html_node(self)
        return node.to_html()
        
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node_list.append(old_node)
        else:
            if delimiter not in old_node.text:
                new_node_list.append(old_node)                
            else:
                split_node = old_node.text.split(delimiter)
                if len(split_node) % 2 == 0:
                   raise Exception(f"no closing delimiter in {old_node}")
                for idx, text in enumerate(split_node):
                    if idx % 2 == 0:
                        node = TextNode(text, TextType.TEXT)
                        new_node_list.append(node)
                    else:
                        node = TextNode(text, text_type)
                        new_node_list.append(node)
    return new_node_list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
        else:
            text = node.text
            while True:
                matches = extract_markdown_images(text)
                if not matches:
                    if text:
                        node_list.append(TextNode(text, TextType.TEXT))
                    break
                else:                    
                    alt, url = matches[0]
                    needle = f"![{alt}]({url})"
                    if needle not in text:
                        node_list.append(TextNode(text, TextType.TEXT))
                        break
                    else:
                        before, after = text.split(needle, 1)
                        if before:
                            node_list.append(TextNode(before, TextType.TEXT))
                        node_list.append(TextNode(alt, TextType.IMAGE, url))                           
                        text = after
                        continue
    return node_list                     

def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
        else:
            text = node.text
            while True:
                matches = extract_markdown_links(text)
                if not matches:
                    if text:
                        node_list.append(TextNode(text, TextType.TEXT))
                    break
                else:                    
                    title, url = matches[0]
                    needle = "[" + title + "](" + url + ")"
                    if needle not in text:
                        node_list.append(TextNode(text, TextType.TEXT))
                        break
                    else:
                        before, after = text.split(needle, 1)
                        if before:
                            node_list.append(TextNode(before, TextType.TEXT))
                        node_list.append(TextNode(title, TextType.LINK, url))                           
                        text = after
                        continue
    return node_list

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text)
        return node
    elif text_node.text_type == TextType.BOLD:
        node = LeafNode("b", text_node.text)
        return node
    elif text_node.text_type == TextType.ITALIC:
        node = LeafNode("i", text_node.text)
        return node
    elif text_node.text_type == TextType.CODE:
        node = LeafNode("code", text_node.text)
        return node
    elif text_node.text_type == TextType.LINK:
        node = LeafNode("a", f"{text_node.text}", props = {'href': text_node.url})
        return node
    elif text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", "",props={'src': text_node.url, 'alt':text_node.text })
        return node                

def text_to_text_nodes(text):
    node = TextNode(text=text, text_type=TextType.TEXT)
    nodes = split_nodes_delimiter([node],"`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        b = block.strip()
        if b:
            blocks.append(b)
    return blocks

def extract_title(markdown):
    match = re.match(r'^#\s+(.*)', markdown)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("no h1 header")

