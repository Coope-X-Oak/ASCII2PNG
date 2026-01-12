from typing import Tuple, Union
from PIL import ImageColor

def hex_to_rgb(color: str) -> Tuple[int, int, int]:
    """
    Convert hex color string to RGB tuple.
    Supports '#RRGGBB' and 'RRGGBB' formats.
    """
    if not color:
        return (0, 0, 0)
    
    # Use PIL for robust parsing if possible, or fallback to manual
    try:
        return ImageColor.getrgb(color)
    except ValueError:
        # Fallback for simple hex without #
        color = color.lstrip('#')
        if len(color) == 6:
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        raise ValueError(f"Invalid color format: {color}")
