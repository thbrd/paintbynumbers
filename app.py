from flask import Flask, request, send_file
from flask_cors import CORS
import os
import uuid
import main

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
    size = int(request.form.get('size', 500))

    if file:
        filename = f"{uuid.uuid4().hex}"
        input_path = os.path.join(UPLOAD_FOLDER, f"{filename}.jpg")
        file.save(input_path)

        output_png = os.path.join(RESULT_FOLDER, f"{filename}.png")
        output_svg = os.path.join(RESULT_FOLDER, f"{filename}.svg")

        main.run_pipeline(input_path, output_png, output_svg, num_colors, size)

        return send_file(output_png, mimetype='image/png')

    return {'error': 'No file uploaded'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
