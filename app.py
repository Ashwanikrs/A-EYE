

import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import generate  # Backend caption generation logic
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Handle file upload and caption generation
@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Generate caption using the backend
        caption = generate.runModel(file_path)

        # Return template with the filename and caption
        return render_template('index.html', filename=filename, caption=caption)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use the PORT variable, default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=True)
