import io
import qrcode
from flask import Blueprint, render_template, request, send_file, jsonify

qrcode_bp = Blueprint('qrcode', __name__)

@qrcode_bp.route('/qrcode-generator')
def ui():
    return render_template('qrcode.html')

@qrcode_bp.route('/api/generate-qr', methods=['POST'])
def api():
    data = request.form.get('data')
    
    if not data:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 1. Create QR Code Object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # 2. Generate Image (In Memory)
        img = qr.make_image(fill_color="black", back_color="white")

        # 3. Save to Byte Buffer (RAM)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # 4. Send to User
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name="qrcode.png"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500