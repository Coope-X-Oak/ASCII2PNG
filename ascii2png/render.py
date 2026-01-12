import io
import os
import time
import hashlib
import math
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from .layout import Scene
from .fonts import get_font, get_title_font, get_body_font

def draw_line_styled(draw, start, end, style="solid", width=2, color="black"):
    x1, y1 = start
    x2, y2 = end
    
    if style == "solid":
        draw.line([start, end], fill=color, width=width)
    elif style == "dotted":
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0: return
        steps = int(length / (width * 3))
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            px = x1 + dx * t
            py = y1 + dy * t
            r = width / 2
            draw.ellipse([px-r, py-r, px+r, py+r], fill=color)
    elif style == "dashed":
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0: return
        dash_len = width * 4
        gap_len = width * 2
        total_cycle = dash_len + gap_len
        
        current = 0
        while current < length:
            t1 = current / length
            t2 = min(current + dash_len, length) / length
            p1 = (x1 + dx * t1, y1 + dy * t1)
            p2 = (x1 + dx * t2, y1 + dy * t2)
            draw.line([p1, p2], fill=color, width=width)
            current += total_cycle
    elif style == "wave":
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        steps = int(length / 2)
        amplitude = width * 2
        frequency = 0.3
        points = []
        for i in range(steps):
            dist = i * 2
            offset = math.sin(dist * frequency) * amplitude
            ox = -math.sin(angle) * offset
            oy = math.cos(angle) * offset
            px = x1 + math.cos(angle) * dist + ox
            py = y1 + math.sin(angle) * dist + oy
            points.append((px, py))
        if len(points) > 1:
            draw.line(points, fill=color, width=width)
    elif style == "cloud":
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length > 0:
            angle = math.atan2(dy, dx)
            radius = width * 4
            step = radius * 1.5
            steps = int(length / step)
            deg = math.degrees(angle)
            for i in range(steps + 1):
                t = i * step
                if t >= length: break
                cx = x1 + math.cos(angle) * (t + radius/2)
                cy = y1 + math.sin(angle) * (t + radius/2)
                ox = -math.sin(angle) * (radius * 0.2)
                oy = math.cos(angle) * (radius * 0.2)
                bbox = [cx + ox - radius/2, cy + oy - radius/2, cx + ox + radius/2, cy + oy + radius/2]
                draw.arc(bbox, deg + 180, deg + 360, fill=color, width=width)

def draw_text_vertical(draw, xy, text, font, fill, spacing=4):
    x, y = xy
    current_y = y
    for char in text:
        bbox = font.getbbox(char)
        # bbox: left, top, right, bottom relative to anchor
        # width = right - left
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        # Draw centered horizontally at x
        draw.text((x - w/2, current_y), char, font=font, fill=fill)
        current_y += font.size + spacing

def draw_text_horizontal_spaced(draw, xy, text, font, fill, spacing=0):
    if spacing == 0:
        draw.text(xy, text, font=font, fill=fill)
        return
    x, y = xy
    current_x = x
    for char in text:
        draw.text((current_x, y), char, font=font, fill=fill)
        w = font.getlength(char)
        current_x += w + spacing

def _font(font_size: int, font_path: str = None) -> ImageFont.FreeTypeFont:
    # Legacy wrapper for backward compatibility
    if font_path:
        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            pass
    return get_font("sans", font_size)

def render_scene(scene: Scene, width: int, text_for_summary: str, output_dir: str, font_path: str = None) -> str:
    scale = 2.0
    w = width
    h = max(scene.height, 400)
    W = int(w * scale)
    H = int(h * scale)
    img = Image.new("RGB", (W, H), scene.bg)
    draw = ImageDraw.Draw(img)
    
    # Check layout mode
    cfg = getattr(scene, "extra_config", {})
    layout_mode = cfg.get("layout_mode", "horizontal")
    
    # --- Background Decoration ---
    if hasattr(scene, "bg_style"):
        style = scene.bg_style
        
        if style == "grid":
            grid_color = cfg.get("grid_color", (220, 220, 220))
            step = int(40 * scale)
            for x in range(0, W, step):
                draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
            for y in range(0, H, step):
                draw.line([(0, y), (W, y)], fill=grid_color, width=1)
                
        elif style == "dots":
            dot_color = cfg.get("dot_color", (200, 200, 200))
            step = int(30 * scale)
            radius = int(2 * scale)
            for x in range(step // 2, W, step):
                for y in range(step // 2, H, step):
                    draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=dot_color)
                    
        elif style == "circle":
            colors = cfg.get("circle_colors", [(240, 240, 240)])
            import random
            rng = random.Random(42)
            for _ in range(5):
                cx = rng.randint(0, W)
                cy = rng.randint(0, H)
                r = rng.randint(int(100 * scale), int(400 * scale))
                c = colors[rng.randint(0, len(colors)-1)]
                draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=c)
        
        elif style == "gradient_green":
            top_c = (240, 253, 244)
            bot_c = (220, 252, 231)
            for y in range(H):
                ratio = y / H
                r = int(top_c[0] + (bot_c[0] - top_c[0]) * ratio)
                g = int(top_c[1] + (bot_c[1] - top_c[1]) * ratio)
                b = int(top_c[2] + (bot_c[2] - top_c[2]) * ratio)
                draw.line([(0, y), (W, y)], fill=(r, g, b), width=1)
    # --- End Background ---

    # Draw Lines
    for line in scene.lines:
        style = getattr(line, "style", "solid")
        draw_line_styled(
            draw,
            (line.x1 * scale, line.y1 * scale),
            (line.x2 * scale, line.y2 * scale),
            style=style,
            width=max(1, int(line.width * scale)),
            color=line.color
        )

    # Draw Texts
    for t in scene.texts:
        size = int(t.size * scale)
        if font_path:
            f = _font(size, font_path)
        else:
            font_style = getattr(t, "font_style", "sans")
            f = get_font(font_style, size)
            
        xy = (int(t.x * scale), int(t.y * scale))
        
        if layout_mode == "vertical":
            s = int(getattr(t, "spacing", 4) * scale)
            draw_text_vertical(draw, xy, t.text, f, t.color, spacing=s)
        else:
            s = int(getattr(t, "spacing", 0) * scale)
            draw_text_horizontal_spaced(draw, xy, t.text, f, t.color, spacing=s)

    out = img.resize((w, H // int(scale)), resample=Image.LANCZOS)
    path = _save_png(out, text_for_summary, output_dir)
    
    if os.path.getsize(path) > 1_000_000:
        path = _shrink_png(out, text_for_summary, output_dir)
    return path

def _save_png(img: Image.Image, text: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    summary = _summary(text)
    name = f"{ts}_{summary}.png"
    path = os.path.join(output_dir, name)
    img.save(path, format="PNG", optimize=True, compress_level=9)
    return path

def _shrink_png(img: Image.Image, text: str, output_dir: str) -> str:
    target = 1_000_000
    os.makedirs(output_dir, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    summary = _summary(text)
    base = f"{ts}_{summary}"
    attempt = 0
    current = img
    while attempt < 5:
        palette = current.convert("P", palette=Image.ADAPTIVE, colors=max(32, 256 // (attempt + 1)))
        path = os.path.join(output_dir, f"{base}_opt{attempt}.png")
        palette.save(path, format="PNG", optimize=True, compress_level=9)
        if os.path.getsize(path) <= target:
            return path
        current = current.resize((int(current.width * 0.9), int(current.height * 0.9)), Image.LANCZOS)
        attempt += 1
    path = os.path.join(output_dir, f"{base}_final.png")
    current.save(path, format="PNG", optimize=True, compress_level=9)
    return path

def _summary(text: str) -> str:
    s = "".join(ch for ch in text.strip().splitlines()[0] if ch.isalnum() or ch in ("-", "_"))
    s = s[:24] if s else "diagram"
    h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:6]
    return f"{s}_{h}"
