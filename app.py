import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from yolo_detection import process_uploaded_video

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video uploaded"
    
    file = request.files['video']
    if file.filename == '' or not allowed_file(file.filename):
        return "Invalid video file"

    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    # Process uploaded video and get unique output name
    output_name = process_uploaded_video(video_path)

    if not output_name:
        return "Error processing video", 500  # Return an error if processing fails

    print(f"Output video name: {output_name}")  # Debugging log

    return redirect(url_for('result', filename=filename, output=output_name))

@app.route('/result')
def result():
    filename = request.args.get('filename')
    output_name = request.args.get('output')
    if not filename or not output_name:
        return "No filename or output name provided", 400

    original_video_url = url_for('static', filename=f'uploads/{filename}')
    processed_video_url = url_for('static', filename=f'uploads/{output_name}')

    return render_template('result.html',
                           original_video_url=original_video_url,
                           processed_video_url=processed_video_url)

if __name__ == '__main__':
    app.run(debug=True)
