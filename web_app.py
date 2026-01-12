from flask import Flask, render_template, request, send_file, jsonify
import os
import time
from PIL import ImageColor
from ascii2png.parser import parse
from ascii2png.layout import layout_tree
from ascii2png.render import render_scene
from ascii2png.theme import get_theme

app = Flask(__name__)

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        theme_name = data.get('theme', 'minimal')
        width = int(data.get('width', 1080))
        
        # Extended options
        layout_mode = data.get('layout_mode', 'horizontal')
        line_style = data.get('line_style', 'solid')
        line_color = data.get('line_color')
        
        if not text.strip():
            return jsonify({'error': 'Input text cannot be empty'}), 400

        # Parse and Generate
        root = parse(text)
        
        # Font size fixed for web demo or adjustable? Let's fix it for now or use default
        font_size = 24
        
        # Get Theme
        colors = get_theme(theme_name, font_size)
        
        # Apply extended options
        colors["layout_mode"] = layout_mode
        colors["line_style"] = line_style
        if line_color:
             try:
                colors["line"] = ImageColor.getrgb(line_color)
             except ValueError:
                pass
        
        # Layout
        scene = layout_tree(root, width, colors["font_size"], colors)
        
        # Render
        # We need a unique filename for the web session
        timestamp = int(time.time() * 1000)
        # Using a temporary output path logic handled by render_scene, but we want to know the file
        # render_scene returns the full path
        path = render_scene(scene, width, f"web_{timestamp}", OUTPUT_DIR)
        
        # Return the filename to be served
        filename = os.path.basename(path)
        return jsonify({'image_url': f'/output/{filename}', 'filename': filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output/<filename>')
def serve_image(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename))

if __name__ == '__main__':
    print("Starting Web GUI at http://localhost:5000")
    app.run(debug=True, port=5000)
