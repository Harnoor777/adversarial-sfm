from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from reconstruction import reconstruct_3d

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_latest_model():
    """Get the most recent .ply file from output folder"""
    try:
        files = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith('.ply')]
        if not files:
            return None
        files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_FOLDER, x)), reverse=True)
        return files[0]
    except Exception as e:
        print(f"Error getting latest model: {e}")
        return None

@app.route('/')
def index():
    latest_model = get_latest_model()
    return render_template('index.html', latest_model=latest_model)

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400
    
    files = request.files.getlist('images')
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No images selected'}), 400
    
    uploaded_files = []
    
    # Clear previous uploads
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Save new uploads
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filename)
    
    if not uploaded_files:
        return jsonify({'error': 'No valid images uploaded'}), 400
    
    # Trigger reconstruction
    try:
        result = reconstruct_3d(app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
        return jsonify({
            'success': True,
            'message': f'Successfully processed {len(uploaded_files)} images',
            'files': uploaded_files,
            'reconstruction': result,
            'model_filename': result.get('output_filename')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download_model(filename):
    """Download a 3D model file"""
    try:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/latest-model')
def api_latest_model():
    """API endpoint to get the latest model info"""
    latest_model = get_latest_model()
    if latest_model:
        file_path = os.path.join(OUTPUT_FOLDER, latest_model)
        file_size = os.path.getsize(file_path)
        file_time = os.path.getmtime(file_path)
        return jsonify({
            'filename': latest_model,
            'size': file_size,
            'timestamp': file_time
        })
    return jsonify({'filename': None})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
