import sys
import asyncio
from flask import Flask, render_template
# Import the blueprint we just created
from routes.audiobook_routes import audio_bp

# Windows Fix for Event Loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)

# --- REGISTER BLUEPRINTS ---
# This adds the Audiobook "Department" to your website
app.register_blueprint(audio_bp)

# --- MAIN DASHBOARD ---
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)