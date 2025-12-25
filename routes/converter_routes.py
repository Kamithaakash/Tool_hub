import io
import pdfplumber
from flask import Blueprint, render_template, request, send_file, jsonify
from docx import Document

converter_bp = Blueprint('converter', __name__)

@converter_bp.route('/file-converter')
def ui():
    return render_template('converter.html')

@converter_bp.route('/api/convert-pdf', methods=['POST'])
def api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 1. Open the PDF directly from the upload stream (RAM)
        with pdfplumber.open(file.stream) as pdf:
            # Create a new Word Document
            doc = Document()
            
            # Extract text page by page
            text_found = False
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    doc.add_paragraph(text)
                    text_found = True
            
            if not text_found:
                return jsonify({"error": "No text found in PDF (It might be an image scan)"}), 400

            # 2. Save DOCX to a Memory Buffer
            docx_io = io.BytesIO()
            doc.save(docx_io)
            docx_io.seek(0) # Rewind buffer to start

            # 3. Send file back to user
            return send_file(
                docx_io,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=f"{file.filename.rsplit('.', 1)[0]}.docx"
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500