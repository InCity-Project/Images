from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Resimlerin kaydedileceği dizin
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No image file selected'}), 400

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    return jsonify({'image_url': f'/images/{image.filename}'})

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Requesting file: {filename}")
    print(f"Full file path: {file_path}")
    
    if not os.path.exists(file_path):
        print("File not found")
        return jsonify({'error': 'File not found'}), 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
