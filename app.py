from flask import Flask, request, send_file, jsonify
import os
import uuid
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    num_colors = int(request.form.get('colors', 24))
    size = 500

    if file:
        file_id = uuid.uuid4().hex
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.jpg")
        output_prefix = os.path.join(RESULT_FOLDER, f"{file_id}")
        output_png = f"{output_prefix}.png"
        output_svg = f"{output_prefix}.svg"

        file.save(input_path)

        cmd = [
            "python3", "main.py",
            "--input", input_path,
            "--output", output_prefix,
            "--colors", str(num_colors),
            "--size", str(size),
            "--svg"
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Verwerking mislukt: {str(e)}"}), 500

        return send_file(output_png, mimetype='image/png')

    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
