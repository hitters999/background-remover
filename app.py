from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import rembg
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'success',
        'message': 'Background Remover API is running',
        'endpoints': {
            'remove': '/api/remove',
            'health': '/api/health'
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'background-remover',
        'version': '1.0.0'
    })

@app.route('/api/remove', methods=['POST'])
def remove_background():
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, GIF, BMP, WEBP'}), 400
        
        # Read image
        image_data = file.read()
        
        # Remove background using rembg
        output = rembg.remove(image_data)
        
        # Convert to PIL Image for optimization
        output_image = Image.open(io.BytesIO(output)).convert('RGBA')
        
        # Save to bytes
        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format='PNG', optimize=True, quality=95)
        output_bytes.seek(0)
        
        return send_file(
            output_bytes,
            mimetype='image/png',
            as_attachment=True,
            download_name='image_no_background.png'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        'service': 'Background Remover',
        'ai_model': 'rembg',
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': MAX_FILE_SIZE // (1024 * 1024),
        'processing': 'AI-powered with rembg',
        'output_format': 'PNG with transparency',
        'quality': 'Ultra HD'
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
