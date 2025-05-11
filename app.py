from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from utils.detection import detect_diseases  # 假设你有这个检测函数

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# 确保上传和结果目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # 病害检测
        result = detect_diseases(upload_path)
        result_image = os.path.join(app.config['RESULT_FOLDER'], filename)

        return jsonify({
            'status': 'success',
            'result': result,
            'original_image': f'/static/uploads/{filename}',
            'result_image': f'/static/results/{filename}'
        })

    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)