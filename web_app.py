from flask import Flask, render_template, request, send_file, jsonify
import os
import sys
import time
import glob
from ascii2png.core import CoreService
from ascii2png.utils import hex_to_rgb

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize Flask with explicit folder paths
app = Flask(__name__, 
            template_folder=resource_path('templates'), 
            static_folder=resource_path('static'))

# Ensure output directory exists
if getattr(sys, 'frozen', False):
    # If frozen, use the directory of the executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # If running as script, use the directory of the script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def cleanup_old_files(max_age_seconds=3600):
    """Delete files older than max_age_seconds in OUTPUT_DIR"""
    try:
        now = time.time()
        for f in glob.glob(os.path.join(OUTPUT_DIR, "web_*.png")):
            if os.path.isfile(f):
                if now - os.path.getmtime(f) > max_age_seconds:
                    try:
                        os.remove(f)
                    except OSError:
                        pass
    except Exception:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Cleanup old files on every request (simple approach)
    # Ideally this should be a background task
    cleanup_old_files()

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

        # Prepare options
        layout_options = {
            "layout_mode": layout_mode,
            "line_style": line_style
        }
        
        custom_colors = {}
        if line_color:
             try:
                rgb = hex_to_rgb(line_color)
                custom_colors["line"] = rgb
             except ValueError:
                pass
        
        # We need a unique filename for the web session
        timestamp = int(time.time() * 1000)
        filename_hint = f"web_{timestamp}"
        
        # Use CoreService
        path = CoreService.convert(
            text=text,
            width=width,
            theme=theme_name,
            font_size=24, # Fixed for web demo as per original
            output_dir=OUTPUT_DIR,
            custom_colors=custom_colors if custom_colors else None,
            layout_options=layout_options,
            filename_hint=filename_hint
        )
        
        # Return the filename to be served
        filename = os.path.basename(path)
        return jsonify({'image_url': f'/output/{filename}', 'filename': filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output/<filename>')
def serve_image(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename))

if __name__ == '__main__':
    port = 5000
    url = f"http://localhost:{port}"
    print(f"Starting Web GUI at {url}")
    
    # Auto open browser
    import webbrowser
    from threading import Timer
    def open_browser():
        webbrowser.open_new(url)
    Timer(1.5, open_browser).start()
    
    # Disable debug mode for production-like usage
    app.run(debug=False, port=port)
