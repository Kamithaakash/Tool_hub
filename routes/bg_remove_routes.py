import os
import io
# --- THE FIX: Disable Numba Parallelism ---
# This prevents the "Freezing" / Infinite loop on Windows
os.environ["NUMBA_NUM_THREADS"] = "1"

from flask import Blueprint, render_template, request, send_file, jsonify
from rembg import remove
from PIL import Image

bg_remove_bp = Blueprint('bg_remove', __name__)

@bg_remove_bp.route('/remove-background')
def ui():
    return render_template('bg_remover.html')

@bg_remove_bp.route('/api/remove-bg', methods=['POST'])
def api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 1. Load image directly from upload stream
        input_image = Image.open(file.stream)

        # 2. Process with AI
        # alpha_matting=True makes edges look better
        output_image = remove(input_image, alpha_matting=True)

        # 3. Save result to a MEMORY buffer
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        # 4. Stream back to user
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f"clean_{file.filename.rsplit('.', 1)[0]}.png"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500