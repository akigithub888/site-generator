import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("text node", TextType.ITALIC)
        node2 = TextNode("text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)
    
    def test_url_none(self):
        node = TextNode("some code", TextType.CODE)
        self.assertIsNone(node.url)
        self.assertEqual(node.text, "some code")
        self.assertEqual(node.text_type, TextType.CODE)
    
    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("Hello `world` and `universe`!", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        assert len(result) == 5
        assert result[0].text == "Hello "
        assert result[0].text_type == TextType.TEXT 
        assert result[1].text == "world"
        assert result[1].text_type == TextType.CODE
        assert result[2].text == " and "
        assert result[2].text_type == TextType.TEXT
        assert result[3].text == "universe"
        assert result[3].text_type == TextType.CODE
        assert result[4].text == "!"
        assert result[4].text_type == TextType.TEXT

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("Check out [Boot.dev](https://boot.dev) for coding!")
        self.assertListEqual([("Boot.dev", "https://boot.dev")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text has no links at all.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_images(self):
        text = "Here's a ![image](https://example.com/pic.jpg) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "![first](https://example.com/1.jpg) and ![second](https://example.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "https://example.com/1.jpg"), ("second", "https://example.com/2.png")], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/image.jpg)")
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_none(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)
    
    def test_split_images_single_middle(self):
        node = TextNode("Start ![alt](http://a.com/x.png) end", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result[0], TextNode("Start ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("alt", TextType.IMAGE, "http://a.com/x.png"))
        self.assertEqual(result[2], TextNode(" end", TextType.TEXT))

    def test_split_images_keeps_other_types(self):
        nodes = [
            TextNode("x ![a](u) y", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(result[-1], nodes[1])

    def test_text_to_text_nodes(self):
        text ="This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_text_nodes(text)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()