from typing import Optional, Dict, Any
from . import parser
from .layout import layout_tree
from .theme import get_theme
from .render import render_scene

class CoreService:
    @staticmethod
    def convert(
        text: str,
        width: int = 1080,
        theme: str = "wechat",
        font_size: int = 24,
        output_dir: str = "output",
        custom_colors: Optional[Dict[str, Any]] = None,
        font_path: Optional[str] = None,
        layout_options: Optional[Dict[str, Any]] = None,
        filename_hint: str = None
    ) -> str:
        """
        Unified conversion logic for CLI, GUI, and Web.
        """
        # 1. Parse
        root = parser.parse(text)
        
        # 2. Prepare Theme/Colors
        if custom_colors:
            colors = custom_colors.copy()
            colors["font_size"] = font_size
        else:
            colors = get_theme(theme, font_size)
            
        # 3. Apply Layout Options
        if layout_options:
            colors.update(layout_options)
            
        # 4. Layout
        scene = layout_tree(root, width, colors["font_size"], colors)
        
        # 5. Render
        # Use filename_hint as the text_for_summary if provided, to influence naming
        summary_text = filename_hint if filename_hint else text
        path = render_scene(scene, width, summary_text, output_dir, font_path)
        
        return path
