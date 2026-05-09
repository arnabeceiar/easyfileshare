import json
import os
from pathlib import Path

def print_tree_node(node, indent="", is_last=True):
    # If it’s a file, print filename
    if node["type"] == "file":
        marker = "└── " if is_last else "├── "
        print(indent + marker + node["path"])
        return

    # If it’s a dir, print dir name
    if node["type"] == "dir":
        marker = "└── " if is_last else "├── "
        print(indent + marker + node["path"] + "/")

        children = node.get("children", [])
        if not children:
            return

        # Prepare indent for children
        if is_last:
            next_indent = indent + "    "
        else:
            next_indent = indent + "│   "

        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            print_tree_node(child, next_indent, is_last_child)


def load_and_print_tree(tree_file):
    with open(tree_file, "r", encoding="utf-8") as f:
        tree = json.load(f)

    # Create a fake root node for the whole tree
    root_node = {
        "type": "dir",
        "path": tree["root"],
        "children": tree["contents"]  # list of dirs + files
    }

    print(f"Tree for {tree['root']}:")
    print_tree_node(root_node)


if __name__ == "__main__":
    tree_file = "seismic_2026_tree.json"  # adjust to your path
    if Path(tree_file).exists():
        load_and_print_tree(tree_file)
    else:
        print(f"File not found: {tree_file}")