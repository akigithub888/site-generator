from block import markdown_to_html_node
from textnode import extract_title
import os
from main import basepath

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    abs_from_path = os.path.abspath(from_path)
    abs_template_path = os.path.abspath(template_path)
    with open(abs_from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(abs_template_path, "r", encoding="utf-8") as f:
        template = f.read()
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)
    placeholder_title = '{{ Title }}'
    placeholder_content = '{{ Content }}'
    content = template.replace(placeholder_title, title)
    content = content.replace(placeholder_content, html)
    content = content.replace('href="/',f'href="{basepath}')
    content = content.replace('src="/', f'src="{basepath}')
    abs_dest_path = os.path.abspath(dest_path)
    os.makedirs(os.path.dirname(abs_dest_path), exist_ok=True)
    with open(abs_dest_path, "w") as f:
        f.write(content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    def walk(curr_dir):
        for name in os.listdir(curr_dir):
            path = os.path.join(curr_dir, name)
            if os.path.isdir(path):
                walk(path)
            elif os.path.isfile(path) and name == "index.md":
                rel_dir = os.path.relpath(curr_dir, start=dir_path_content)
                des_dir = os.path.join(dest_dir_path, rel_dir)
                os.makedirs(des_dir, exist_ok=True)
                dest_html = os.path.join(des_dir, "index.html")
                generate_page(path, template_path, dest_html)
    walk(dir_path_content)