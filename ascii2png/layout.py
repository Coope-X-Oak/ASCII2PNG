from typing import List, Tuple
from .parser import Node

class VecText:
    def __init__(self, text: str, x: float, y: float, size: int, color: Tuple[int, int, int], font_style: str = "sans", spacing: int = 0):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.font_style = font_style
        self.spacing = spacing

class VecLine:
    def __init__(self, x1: float, y1: float, x2: float, y2: float, width: int, color: Tuple[int, int, int], style: str = "solid"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.color = color
        self.style = style

class Scene:
    def __init__(self, width: int, height: int, bg: Tuple[int, int, int], bg_style: str = "plain", extra_config: dict = None):
        self.width = width
        self.height = height
        self.bg = bg
        self.bg_style = bg_style
        self.extra_config = extra_config or {}
        self.texts: List[VecText] = []
        self.lines: List[VecLine] = []

def layout_tree(root: Node, width: int, font_size: int, colors: dict) -> Scene:
    mode = colors.get("layout_mode", "horizontal")
    if mode == "vertical":
        return layout_tree_rtl(root, width, font_size, colors)
    else:
        return layout_tree_horizontal(root, width, font_size, colors)

def layout_tree_horizontal(root: Node, width: int, font_size: int, colors: dict) -> Scene:
    """
    Standard Vertical List (File Tree).
    """
    x_margin = 40
    y_margin = 40
    line_height = int(font_size * 1.8)
    indent_step = int(font_size * 2.0)
    
    layout_items: List[Tuple[Node, int, float]] = []
    current_y = float(y_margin)
    
    def traverse(node: Node, depth: int):
        nonlocal current_y
        layout_items.append((node, depth, current_y))
        # Add extra spacing for root title?
        spacing = line_height
        if depth == 0:
             spacing = int(line_height * 1.5)
        current_y += spacing
        for child in node.children:
            traverse(child, depth + 1)
            
    traverse(root, 0)
    
    scene_height = int(current_y + y_margin)
    scene = Scene(
        width=width, 
        height=scene_height, 
        bg=colors["bg"], 
        bg_style=colors.get("bg_style", "plain"),
        extra_config=colors
    )
    
    def get_node_y(n: Node) -> float:
        for node, _, y in layout_items:
            if node is n:
                return y
        return 0.0

    line_style = colors.get("line_style", "solid")

    for node, depth, y in layout_items:
        x_text = x_margin + depth * indent_step
        
        # Font styling
        is_root = (depth == 0)
        f_size = int(font_size * 1.5) if is_root else font_size
        f_style = "serif" if is_root else "sans"
        f_spacing = 4 if is_root else 0
        
        # Title specific: Bold is handled by font selection (usually serif is bolder or we can add bold flag)
        # We'll rely on 'serif' font for title.
        
        scene.texts.append(VecText(node.label, x_text, y, f_size, colors["text"], font_style=f_style, spacing=f_spacing))
        
        if node.children:
            child_depth = depth + 1
            vline_x = x_margin + (child_depth * indent_step) - (indent_step / 2)
            
            first_child = node.children[0]
            last_child = node.children[-1]
            
            y_first = get_node_y(first_child)
            y_last = get_node_y(last_child)
            
            half_font = font_size * 0.5
            
            # Vertical backbone
            scene.lines.append(VecLine(
                vline_x, 
                y_first + half_font, 
                vline_x, 
                y_last + half_font, 
                max(2, font_size // 12), 
                colors["line"],
                style=line_style
            ))
            
            # Horizontal connectors
            for child in node.children:
                cy = get_node_y(child)
                child_text_x = x_margin + child_depth * indent_step
                scene.lines.append(VecLine(
                    vline_x, 
                    cy + half_font, 
                    child_text_x - (font_size * 0.2),
                    cy + half_font, 
                    max(2, font_size // 12), 
                    colors["line"],
                    style=line_style
                ))
    return scene

def layout_tree_rtl(root: Node, width: int, font_size: int, colors: dict) -> Scene:
    """
    RTL Vertical Text Layout.
    Columns flow Right-to-Left.
    """
    margin = 60
    col_width = int(font_size * 1.8)
    indent_step = int(font_size * 2.0) # Vertical indent for hierarchy
    
    layout_items = []
    current_x = float(width - margin)
    
    def traverse(node: Node, depth: int):
        nonlocal current_x
        layout_items.append((node, depth, current_x))
        current_x -= col_width
        for child in node.children:
            traverse(child, depth + 1)
            
    traverse(root, 0)
    
    real_min_x = min([item[2] for item in layout_items]) if layout_items else margin
    shift = 0
    if real_min_x < margin:
        shift = margin - real_min_x
        
    scene_width = width
    if shift > 0:
        scene_width = int((width - margin) + shift + margin)
    
    max_y = 0
    
    scene = Scene(
        width=scene_width, 
        height=0, 
        bg=colors["bg"], 
        bg_style=colors.get("bg_style", "plain"),
        extra_config=colors
    )
    
    line_style = colors.get("line_style", "solid")
    
    for node, depth, x in layout_items:
        x = x + shift
        y_start = margin + depth * indent_step
        
        is_root = (depth == 0)
        f_style = "serif" if is_root else "sans"
        f_size = int(font_size * 1.5) if is_root else font_size
        f_spacing = 8 if is_root else 4
        
        scene.texts.append(VecText(
            node.label, 
            x, 
            y_start, 
            f_size, 
            colors["text"], 
            font_style=f_style,
            spacing=f_spacing
        ))
        
        text_len = len(node.label)
        text_height = text_len * (f_size + f_spacing)
        max_y = max(max_y, y_start + text_height)
        
        if node.children:
            child_xs = []
            for c in node.children:
                for n_item, d_item, x_item in layout_items:
                    if n_item is c:
                        child_xs.append(x_item + shift)
                        break
            
            if not child_xs: continue
            
            last_child_x = child_xs[-1] # Leftmost
            
            backbone_y = y_start + (indent_step / 2)
            
            # Horizontal Backbone
            scene.lines.append(VecLine(
                x, 
                backbone_y,
                last_child_x, 
                backbone_y, 
                max(2, font_size // 10), 
                colors["line"],
                style=line_style
            ))
            
            # Vertical Ticks to Children
            for cx in child_xs:
                 scene.lines.append(VecLine(
                    cx,
                    backbone_y,
                    cx,
                    y_start + indent_step, 
                    max(2, font_size // 10),
                    colors["line"],
                    style=line_style
                ))
            
            # Vertical Tick from Parent
            scene.lines.append(VecLine(
                x,
                y_start,
                x,
                backbone_y,
                max(2, font_size // 10),
                colors["line"],
                style=line_style
            ))
            
    scene.height = int(max_y + margin)
    return scene
