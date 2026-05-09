from pathlib import Path
import json
from datetime import datetime, timezone
import os

def scan_subtree(root_path):
    root = Path(root_path).resolve()
    print(f"Scanning subtree at: {root}")

    def relpath_str(path):
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
            print(f"Warning: Path {path} is not relative to root {root}")
        return str(rel).replace("\\", "/") if rel != "." else ""

    for path in root.rglob("*"):
        if not path.exists():
            print(f"Skipping non-existent path: {path}")
            continue
        rel_path = relpath_str(path)
        print(f"Found: {rel_path}")


if __name__ == "__main__":
    root_path = os.getcwd()
    scan_subtree(root_path)



