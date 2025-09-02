from enum import Enum
from htmlnode import *
from textnode import *
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"  
    ULIST = "unordered_list"  

def block_to_block_type(block):
    lines = [line.strip() for line in block.split('\n')]
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    if block.startswith("1. "): # A good first check to quickly rule out non-ordered lists
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH # If any line doesn't match, it's not an ordered list
            i += 1
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    stripped_blocks = [line.strip() for line  in markdown.split('\n\n')]
    blocks = []
    for block in stripped_blocks:
        if block:
            blocks.append(block)
    return blocks

def block_to_text(block, block_type):
    if block_type == BlockType.HEADING:
        return block.lstrip('#').lstrip()
    if block_type == BlockType.CODE:
        lines = block.splitlines()
        middle = lines[1:-1]
        # Compute common leading whitespace across non-empty lines
        def leading_ws(s): 
            return len(s) - len(s.lstrip(" "))
        non_empty = [ln for ln in middle if ln.strip()]
        if non_empty:
            common = min(leading_ws(ln) for ln in non_empty)
            deindented = [ln[common:] if len(ln) >= common else ln for ln in middle]
        else:
            deindented = middle
        content = "\n".join(deindented)
        if not content.endswith("\n"):
            content += "\n"
        return content
        
    if block_type == BlockType.QUOTE:
        lines = [line.removeprefix("> ") for line in block.split('\n')]
        merged = " ".join(lines)
        return merged
    if block_type == BlockType.ULIST:
        lines = []
        for line in block.split('\n'):
            for prefix in ("- ", "+ ", "* "):
                if line.startswith(prefix):
                    line = line.removeprefix(prefix)
                    break  # stop checking once one prefix is removed
            lines.append(line)
        #merged = "\n".join(lines)
        return lines
    if block_type == BlockType.OLIST:
        lines = [line.strip() for line in block.split('\n')]
        clean_lines = []
        for line in lines:
            index = line.find(".")
            clean_line = line[index+2:]
            clean_lines.append(clean_line)
        #merged = "\n".join(clean_lines)
        return clean_lines
    if block_type == BlockType.PARAGRAPH:
        lines = block.splitlines()
        trimmed = [line.strip() for line in lines]
        non_empty = [line for line in trimmed if line]
        return " ".join(non_empty)

def text_to_children(text):
    text_node_list = text_to_text_nodes(text)
    children_list = []
    for node in text_node_list:
        html_node = text_node_to_html_node(node)
        children_list.append(html_node)
    return children_list

def heading_counter(block):
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            break
    return count


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        text = block_to_text(block, block_type)
        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(text)
            node = ParentNode("p", children=children)
        elif block_type == BlockType.HEADING:
            children = text_to_children(text)
            node = ParentNode(tag=f"h{heading_counter(block)}",children=children)
        elif block_type == BlockType.QUOTE:
            children = text_to_children(text)
            node = ParentNode(tag="blockquote",children=children)
        elif block_type == BlockType.ULIST:
            list_item_nodes = []
            for item_string in text:
                item_children = text_to_children(item_string)
                node = ParentNode(tag="li", children=item_children)
                list_item_nodes.append(node)
            node = ParentNode(tag="ul", children=list_item_nodes)
        elif block_type == BlockType.OLIST:
            list_item_nodes = []
            for item_string in text:
                item_children = text_to_children(item_string)
                node = ParentNode(tag="li", children=item_children)
                list_item_nodes.append(node)
            node = ParentNode(tag="ol", children=list_item_nodes)
        elif block_type == BlockType.CODE:
            text_node = TextNode(text=text, text_type=TextType.TEXT)
            code_node = LeafNode("code", text_node.text)
            node = ParentNode("pre", [code_node])
        children_nodes.append(node)
    parent_node = ParentNode("div", children=children_nodes)
    return parent_node