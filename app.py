import sys
import asyncio
import os
from flask import Flask, render_template
# Import the blueprint we just created
from routes.audiobook_routes import audio_bp
from routes.bg_remove_routes import bg_remove_bp
from routes.qrcode_routes import qrcode_bp
from routes.converter_routes import converter_bp


# Windows Fix for Event Loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)

# --- REGISTER BLUEPRINTS ---
# This adds the Audiobook "Department" to your website

app.register_blueprint(audio_bp)
app.register_blueprint(bg_remove_bp)
app.register_blueprint(qrcode_bp)
app.register_blueprint(converter_bp)

# --- MAIN DASHBOARD ---
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    # Get the PORT from the server, or default to 5000 if running locally
    port = int(os.environ.get("PORT", 5000))
    # Host must be '0.0.0.0' to be visible on the internet
    app.run(host='0.0.0.0', port=port, debug=False)