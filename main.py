import argparse
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from ascii2png import parser
from ascii2png.layout import layout_tree
from ascii2png.theme import get_theme
from ascii2png.render import render_scene
from ascii2png.utils import read_text, list_inputs


def convert_text(text: str, width: int, theme: str, font_size: int, output_dir: str, custom_colors: dict = None, font_path: str = None, layout_options: dict = None) -> str:
    root = parser.parse(text)
    if custom_colors:
        colors = custom_colors
        colors["font_size"] = font_size
    else:
        colors = get_theme(theme, font_size)
    
    if layout_options:
        colors.update(layout_options)

    scene = layout_tree(root, width, colors["font_size"], colors)
    path = render_scene(scene, width, text, output_dir, font_path)
    return path


def run_cli(args: argparse.Namespace):
    outdir = args.output or os.path.join(os.getcwd(), "output")
    width = args.width or 1080
    theme = args.theme or "wechat"
    font_size = args.font or 24
    if args.text:
        path = convert_text(args.text, width, theme, font_size, outdir)
        print(path)
        return
    if args.input and os.path.isfile(args.input):
        txt = read_text(args.input)
        path = convert_text(txt, width, theme, font_size, outdir)
        print(path)
        return
    if args.batch and os.path.isdir(args.batch):
        files = list_inputs(args.batch)
        if not files:
            print("未在输入目录发现文本文件")
            return
        for f in files:
            try:
                txt = read_text(f)
                p = convert_text(txt, width, theme, font_size, outdir)
                print(p)
            except Exception as e:
                print(f"处理失败: {f}: {e}")
        return
    print("请使用 --text 或 --input 文件，或 --batch 目录")


def run_gui():
    app = tk.Tk()
    app.title("ASCII 图表转 PNG")
    app.geometry("1000x750")
    
    main_frame = ttk.Frame(app, padding=12)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # --- Top Control Panel ---
    controls = ttk.LabelFrame(main_frame, text="配置", padding=10)
    controls.pack(fill=tk.X, pady=(0, 10))
    
    # Row 1: Basic Settings
    row1 = ttk.Frame(controls)
    row1.pack(fill=tk.X, pady=2)
    
    ttk.Label(row1, text="字体大小:").pack(side=tk.LEFT)
    font_var = tk.IntVar(value=24)
    ttk.Spinbox(row1, from_=14, to=72, textvariable=font_var, width=5).pack(side=tk.LEFT, padx=5)
    
    ttk.Label(row1, text="输出宽度:").pack(side=tk.LEFT, padx=(15, 0))
    width_var = tk.IntVar(value=1080)
    ttk.Spinbox(row1, from_=480, to=3840, textvariable=width_var, width=6).pack(side=tk.LEFT, padx=5)

    outdir_var = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
    def choose_dir():
        d = filedialog.askdirectory()
        if d: outdir_var.set(d)
    ttk.Label(row1, text="输出目录:").pack(side=tk.LEFT, padx=(15, 0))
    ttk.Entry(row1, textvariable=outdir_var, width=30).pack(side=tk.LEFT, padx=5)
    ttk.Button(row1, text="浏览", command=choose_dir).pack(side=tk.LEFT)

    # Row 1.5: Layout Settings
    row_layout = ttk.Frame(controls)
    row_layout.pack(fill=tk.X, pady=2)

    ttk.Label(row_layout, text="排版模式:").pack(side=tk.LEFT)
    layout_mode_var = tk.StringVar(value="horizontal")
    ttk.Combobox(row_layout, textvariable=layout_mode_var, values=["horizontal", "vertical"], state="readonly", width=10).pack(side=tk.LEFT, padx=5)

    ttk.Label(row_layout, text="线条样式:").pack(side=tk.LEFT, padx=(15, 0))
    line_style_var = tk.StringVar(value="solid")
    ttk.Combobox(row_layout, textvariable=line_style_var, values=["solid", "dotted", "dashed", "wave", "cloud"], state="readonly", width=10).pack(side=tk.LEFT, padx=5)

    # Row 2: Theme Settings
    row2 = ttk.Frame(controls)
    row2.pack(fill=tk.X, pady=10)
    
    use_custom = tk.BooleanVar(value=False)
    
    # Preset Theme Area
    preset_frame = ttk.Frame(row2)
    preset_frame.pack(side=tk.LEFT)
    ttk.Label(preset_frame, text="预设主题:").pack(side=tk.LEFT)
    theme_var = tk.StringVar(value="wechat")
    theme_combo = ttk.Combobox(preset_frame, textvariable=theme_var, values=["wechat", "light", "dark"], state="readonly", width=10)
    theme_combo.pack(side=tk.LEFT, padx=5)

    # Separator
    ttk.Separator(row2, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=20)
    
    # Custom Theme Area
    custom_frame = ttk.Frame(row2)
    custom_frame.pack(side=tk.LEFT)
    
    # Variables for custom colors
    bg_color = tk.StringVar(value="#FFFFFF")
    text_color = tk.StringVar(value="#333333")
    line_color = tk.StringVar(value="#BBBBBB")
    font_path_var = tk.StringVar(value="")

    def pick_color(var):
        c = colorchooser.askcolor(color=var.get(), title="选择颜色")
        if c[1]: var.set(c[1])
        
    def pick_font():
        f = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf;*.ttc;*.otf")])
        if f: font_path_var.set(f)

    def toggle_custom():
        is_custom = use_custom.get()
        state = "normal" if is_custom else "disabled"
        # Enable/Disable Custom widgets
        btn_bg.configure(state=state)
        btn_text.configure(state=state)
        btn_line.configure(state=state)
        btn_font.configure(state=state)
        # Disable/Enable Preset
        theme_combo.configure(state="disabled" if is_custom else "readonly")

    ttk.Checkbutton(custom_frame, text="自定义风格", variable=use_custom, command=toggle_custom).pack(side=tk.LEFT, padx=(0, 10))
    
    # Color Pickers
    btn_bg = ttk.Button(custom_frame, text="背景色", command=lambda: pick_color(bg_color), state="disabled")
    btn_bg.pack(side=tk.LEFT, padx=2)
    btn_text = ttk.Button(custom_frame, text="文字色", command=lambda: pick_color(text_color), state="disabled")
    btn_text.pack(side=tk.LEFT, padx=2)
    btn_line = ttk.Button(custom_frame, text="线条色", command=lambda: pick_color(line_color), state="disabled")
    btn_line.pack(side=tk.LEFT, padx=2)
    
    # Font File
    btn_font = ttk.Button(custom_frame, text="选择字体文件...", command=pick_font, state="disabled")
    btn_font.pack(side=tk.LEFT, padx=10)
    ttk.Label(custom_frame, textvariable=font_path_var, foreground="gray").pack(side=tk.LEFT)

    # --- Text Input ---
    txt_frame = ttk.LabelFrame(main_frame, text="输入 ASCII 内容", padding=10)
    txt_frame.pack(fill=tk.BOTH, expand=True)
    
    txt = tk.Text(txt_frame, wrap=tk.NONE, font=("Consolas", 12))
    txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scroll_y = ttk.Scrollbar(txt_frame, orient=tk.VERTICAL, command=txt.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    txt.configure(yscrollcommand=scroll_y.set)

    # --- Bottom Buttons ---
    btn_frame = ttk.Frame(main_frame, padding=(0, 10))
    btn_frame.pack(fill=tk.X)
    
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def on_generate():
        t = txt.get("1.0", tk.END)
        if not t.strip():
            messagebox.showerror("错误", "请输入 ASCII 图表文本")
            return
            
        custom_cfg = None
        f_path = None
        
        if use_custom.get():
            try:
                custom_cfg = {
                    "bg": hex_to_rgb(bg_color.get()),
                    "text": hex_to_rgb(text_color.get()),
                    "line": hex_to_rgb(line_color.get()),
                    "accent": hex_to_rgb(line_color.get()) # reuse line color for accent for now
                }
                if font_path_var.get():
                    f_path = font_path_var.get()
            except Exception as e:
                messagebox.showerror("配置错误", f"颜色格式错误: {e}")
                return

        try:
            l_opts = {
                "layout_mode": layout_mode_var.get(),
                "line_style": line_style_var.get()
            }
            p = convert_text(
                t, 
                width_var.get(), 
                theme_var.get(), 
                font_var.get(), 
                outdir_var.get(),
                custom_colors=custom_cfg,
                font_path=f_path,
                layout_options=l_opts
            )
            messagebox.showinfo("完成", f"已生成: {p}")
        except Exception as e:
            messagebox.showerror("失败", str(e))

    ttk.Button(btn_frame, text="生成 PNG", command=on_generate).pack(side=tk.RIGHT)

    app.mainloop()


def main():
    parser_cli = argparse.ArgumentParser(description="ASCII 图表转 PNG")
    parser_cli.add_argument("--text", type=str, help="直接输入ASCII文本")
    parser_cli.add_argument("--input", type=str, help="输入文件路径")
    parser_cli.add_argument("--batch", type=str, help="批量处理目录")
    parser_cli.add_argument("--output", type=str, help="输出目录")
    parser_cli.add_argument("--width", type=int, default=1080, help="输出宽度")
    parser_cli.add_argument("--theme", type=str, default="wechat", help="主题: wechat|light|dark")
    parser_cli.add_argument("--font", type=int, default=24, help="字体大小")
    parser_cli.add_argument("--gui", action="store_true", help="启动图形界面")
    args = parser_cli.parse_args()
    
    # Default to GUI if no processing arguments are provided
    if args.gui or (not args.text and not args.input and not args.batch):
        run_gui()
    else:
        run_cli(args)


if __name__ == "__main__":
    main()
