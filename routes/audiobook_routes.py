import io
import re
import edge_tts
from flask import Blueprint, render_template, request, send_file, jsonify

audio_bp = Blueprint('audiobook', __name__)

# --- HELPER: Clean Text ---
def clean_text(raw_text):
    if not raw_text: return ""
    text = raw_text.replace('\n\n', '||PARAGRAPH_BREAK||').replace('\n', ' ').replace('||PARAGRAPH_BREAK||', '\n\n')
    return re.sub(' +', ' ', text).strip()

# --- ROUTE: The UI ---
@audio_bp.route('/audiobook')
def ui():
    return render_template('audiobook.html')

# --- ROUTE: The API (Streaming) ---
@audio_bp.route('/api/convert', methods=['POST'])
async def api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    voice = request.form.get('voice', 'en-GB-RyanNeural')
    rate = request.form.get('rate', '+0%')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 1. Process Text
        raw_text = file.read().decode("utf-8")
        final_text = clean_text(raw_text)
        if not final_text: return jsonify({"error": "Empty file"}), 400

        # 2. Generate Audio in MEMORY (RAM) - No Hard Drive Used
        communicate = edge_tts.Communicate(final_text, voice, rate=rate)
        
        # Create a memory buffer
        audio_memory = io.BytesIO()
        
        # Stream chunks into the buffer
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_memory.write(chunk["data"])
        
        # Reset buffer pointer to the beginning
        audio_memory.seek(0)

        # 3. Send directly to browser
        return send_file(
            audio_memory,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="my_audiobook.mp3"
        )

    except Exception as e:
        # If error, we try to return JSON (Frontend handles this)
        return jsonify({"error": str(e)}), 500