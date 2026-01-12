import re
from typing import List, Optional


class Node:
    def __init__(self, label: str):
        self.label = label.strip()
        self.children: List["Node"] = []

    def add_child(self, child: "Node"):
        self.children.append(child)


def parse(text: str) -> Node:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("输入为空或非文本")
    lines = [l.rstrip("\n") for l in text.splitlines() if l.strip()]
    if not lines:
        raise ValueError("未检测到有效内容")
    if _has_box_drawing(lines) or _has_tree_connectors(lines):
        return _parse_tree_style(lines)
    return _parse_indent_style(lines)


def _has_box_drawing(lines: List[str]) -> bool:
    return any(re.search(r"[├└│─┴┬┼]+", l) for l in lines)


def _has_tree_connectors(lines: List[str]) -> bool:
    return any(("├" in l or "└" in l or "│" in l or "──" in l) for l in lines) or any(
        re.search(r"^\s*[\|\+\-]+", l) for l in lines
    )


def _parse_tree_style(lines: List[str]) -> Node:
    root_label = _extract_root_label(lines)
    root = Node(root_label)
    stack: List[tuple[int, Node]] = [(0, root)]
    for line in lines:
        m = re.match(r"^(\s*(?:│\s{3}|\s{4})*)(├──|└──|\|\-|\+\-|\-|\+)?\s*(.*)$", line)
        if not m:
            continue
        indent_str, _, content = m.groups()
        if not content.strip():
            continue
        depth = _depth_from_indent(indent_str)
        node = Node(content)
        while stack and stack[-1][0] >= depth:
            stack.pop()
        parent = stack[-1][1] if stack else root
        parent.add_child(node)
        stack.append((depth, node))
    if not root.children and len(lines) > 1:
        return _parse_indent_style(lines)
    return root


def _parse_indent_style(lines: List[str]) -> Node:
    root = Node(_clean_line(lines[0]))
    stack: List[tuple[int, Node]] = [(0, root)]
    for line in lines[1:]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = _clean_line(line)
        depth = indent // 2 if indent >= 2 else (1 if indent > 0 else 0)
        node = Node(content)
        while stack and stack[-1][0] >= depth:
            stack.pop()
        parent = stack[-1][1] if stack else root
        parent.add_child(node)
        stack.append((depth, node))
    return root


def _extract_root_label(lines: List[str]) -> str:
    for l in lines:
        s = l.strip()
        if s and not re.match(r"^[\|\-\+\s│├└─]+$", s):
            return _clean_line(s)
    return _clean_line(lines[0])


def _depth_from_indent(indent_str: str) -> int:
    if not indent_str:
        return 1
    count = 0
    i = 0
    while i < len(indent_str):
        if indent_str[i:i+4] == "│   ":
            count += 1
            i += 4
        elif indent_str[i:i+4] == "    ":
            count += 1
            i += 4
        else:
            i += 1
    return count + 1


def _clean_line(line: str) -> str:
    s = re.sub(r"^[\|\-\+\s│├└─]+", "", line)
    return s.strip()
