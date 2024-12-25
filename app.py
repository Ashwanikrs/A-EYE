import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import generate  # Backend caption generation logic
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Flask app with flexible paths
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'Templates'),  # Templates directory
    static_folder=os.path.join(BASE_DIR, 'static')       # Static files directory
)

# Directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if os.access(UPLOAD_FOLDER, os.W_OK):
    print(f"Write access to {UPLOAD_FOLDER} is available")
else:
    print(f"Write access to {UPLOAD_FOLDER} is not available")
print(f"Templates folder path: {os.path.join(BASE_DIR, 'templates')}")


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Handle file upload and caption generation
@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'file' not in request.files:
        return "No file part"
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        return "No selected file", 400
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to: {file_path}")
        file.save(file_path)

        # Generate caption using the backend
        # Check if the file is accessible
        if not os.path.exists(file_path):
            return f"File not found at {file_path}", 500
        print(f"File saved successfully at {file_path}")
        # Generate caption
        print("Running model for caption generation...")
        caption = generate.runModel(file_path)
        print(f"Caption generated: {caption}")

        # Return template with the filename and caption
        # Render response
        return render_template('index.html', filename=filename, caption=caption)
    except Exception as e:
        print(f"Error during caption generation: {e}")
        return f"Error: {e}", 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use the PORT variable, default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=False)
