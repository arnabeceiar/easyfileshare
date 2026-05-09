from pathlib import Path
import json
from datetime import datetime, timezone
import os

def scan_subtree_flat(root_path):
    """
    Build a tree as a FLAT list of nodes, each node has:
    - path: relative to root
    - type: "file" or "dir"
    - size, mtime
    """
    root = Path(root_path).resolve()
    nodes = []

    def relpath_str(path):
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
        return str(rel).replace("\\", "/") if rel != "." else ""

    for path in root.rglob("*"):
        if not path.exists():
            continue

        if path.is_dir():
            nodes.append({
                "path": relpath_str(path),
                "type": "dir",
                "size": 0,
                "mtime": int(path.stat().st_mtime),
                "children": None   # no nested list
            })

        elif path.is_file():
            nodes.append({
                "path": relpath_str(path),
                "type": "file",
                "size": path.stat().st_size,
                "mtime": int(path.stat().st_mtime),
                "children": None
            })

    return {
        "root": root.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "contents": nodes   # flat list, no nesting
    }


def save_tree(tree, tree_file):
    with open(tree_file, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)


def load_tree(tree_file):
    with open(tree_file, "r", encoding="utf-8") as f:
        return json.load(f)


# =======================
# Print tree from flat contents
# =======================


def print_tree_flat(tree, top_indent=""):
    """
    Prints tree from a flat list of nodes.
    """
    import os

    def split_to_parts(path):
        parts = []
        rest = path
        if not rest:
            return parts
        while True:
            rest, leaf = os.path.split(rest)
            if leaf:
                parts.append(leaf)
            if not rest:
                break
            if rest.endswith("/") or rest.endswith("\\"):
                rest = rest[:-1]
        return parts[::-1]

    # Build a set of all paths and their types
    path_to_type = {}
    for node in tree["contents"]:
        path = node["path"]
        path_to_type[path] = node["type"]

    # Sort paths so shorter ones come first
    all_paths = list(path_to_type.keys())
    all_paths.sort(key=lambda p: (p.count("/"), p))  # dirs before long files

    last_level = {}
    def compute_level(path):
        if not path:
            return 0
        return path.count("/")

    lines = []
    shown = set()

    for raw_path in all_paths:
        path = raw_path
        if not path or path in shown:
            continue

        parts = split_to_parts(path)
        full = ""
        for i, part in enumerate(parts):
            if i == 0:
                full = part
            else:
                full = f"{full}/{part}"

            if full in shown:
                continue

            shown.add(full)
            level = i
            if path_to_type[full] == "dir":
                if level == 0:
                    lines.append(f"└── {full}/")
                else:
                    prefix = "│   " * (level - 1) + "├── "
                    lines.append(prefix + f"{full}/")
            else:
                if level == 0:
                    lines.append(f"└── {full}")
                else:
                    prefix = "│   " * (level - 1) + "├── "
                    lines.append(prefix + f"{full}")

    # Cosmetic: make first node "└── "
    if lines:
        first_line = lines[0]
        if first_line.startswith("├── "):
            lines[0] = "└── " + first_line[4:]

    for line in lines:
        print(top_indent + line)


if __name__ == "__main__":
    source_dir = os.getcwd() #"D:\\EasyFileShare\\tests"
    tree_file = "seismic_2026_tree.json"

    tree = scan_subtree_flat(source_dir)
    save_tree(tree, tree_file)

    print_tree_flat(tree)