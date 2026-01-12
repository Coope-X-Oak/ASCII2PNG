from typing import Dict, Tuple, Any


def get_theme(name: str, font_size: int) -> Dict[str, Any]:
    n = (name or "minimal").lower()
    
    # Base configuration
    base = {
        "font_size": font_size,
        "bg_style": "plain", # plain, grid, dots, circle, gradient
    }

    if n == "minimal" or n == "简约":
        # 简约风格：白底黑字，无冗余装饰
        return {
            **base,
            "bg": (255, 255, 255),
            "text": (33, 33, 33),
            "line": (200, 200, 200),
            "accent": (100, 100, 100),
            "bg_style": "plain",
        }
    
    if n == "business" or n == "商务":
        # 商务风格：深蓝/灰配色，网格背景
        return {
            **base,
            "bg": (245, 247, 250),
            "text": (44, 62, 80),
            "line": (189, 195, 199),
            "accent": (52, 152, 219),
            "bg_style": "grid",
            "grid_color": (230, 230, 235),
        }
        
    if n == "art" or n == "艺术":
        # 艺术风格：暖色调，圆形装饰
        return {
            **base,
            "bg": (253, 250, 245), # Creamy white
            "text": (93, 64, 55),  # Brownish
            "line": (215, 204, 200),
            "accent": (255, 112, 67),
            "bg_style": "circle",
            "circle_colors": [(255, 224, 178), (255, 204, 188)],
        }
        
    if n == "tech" or n == "科技":
        # 科技风格：暗色模式，霓虹线条，点阵背景
        return {
            **base,
            "bg": (15, 23, 42), # Dark blue/slate
            "text": (226, 232, 240),
            "line": (51, 65, 85),
            "accent": (56, 189, 248), # Cyan
            "bg_style": "dots",
            "dot_color": (30, 41, 59),
        }

    if n == "nature" or n == "自然":
        # 自然风格：绿色系，渐变感
        return {
            **base,
            "bg": (240, 253, 244), # Light green tint
            "text": (20, 83, 45),
            "line": (187, 247, 208),
            "accent": (22, 163, 74),
            "bg_style": "gradient_green",
        }

    # Fallback to Minimal
    return {
        **base,
        "bg": (255, 255, 255),
        "text": (33, 33, 33),
        "line": (200, 200, 200),
        "accent": (100, 100, 100),
        "bg_style": "plain",
    }
