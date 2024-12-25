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


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Handle file upload and caption generation
@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    try:
        # Check filename and secure it
        filename = secure_filename(file.filename)
        logger.debug(f"Secured filename: {filename}")

        # Construct the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.debug(f"Resolved file path: {file_path}")

        # Save the file
        file.save(file_path)
        logger.debug("File save attempted.")

        # Verify file existence after saving
        if os.path.exists(file_path):
            logger.debug(f"File saved successfully at {file_path}")
        else:
            logger.error(f"File save failed. File not found at {file_path}")
            return f"File save failed. File not found at {file_path}", 500

        # Render image preview and caption generation
        return render_template('index.html', filename=filename, caption=None)
    except Exception as e:
        logger.error(f"Exception during file save or processing: {e}")
        return f"Error: {e}", 500




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use the PORT variable, default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=False)
