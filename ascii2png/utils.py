import os
import glob
from typing import List


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def list_inputs(input_dir: str) -> List[str]:
    exts = ("*.txt", "*.asc", "*.ascii", "*.md")
    files: List[str] = []
    for e in exts:
        files += glob.glob(os.path.join(input_dir, e))
    return sorted(files)
