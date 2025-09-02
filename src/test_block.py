import unittest

from block import *


class test_block(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a simple paragraph block."
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_block_type_code(self):
        block = """```python
            def example_function():
            print("Hello, world!")
            ```"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, result)
    
    def test_block_to_block_type_quote(self):
        block = """> This is a quoted line.
        > This is another quoted line."""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_block_type_olist(self):
        block = """1. First item
            2. Second item
            3. Third item"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.OLIST, result)

    def test_markdown_to_blocks_single_block(self):
        md = "This is just one paragraph with no blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just one paragraph with no blank lines."])
    
    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )