from flask import Flask, request, jsonify, send_file
import os
import uuid
from paint_by_numbers import generate_paint_by_numbers

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    num_colors = int(request.form.get('colors', 24))

    if file:
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        output_path = os.path.join(RESULT_FOLDER, f"{filename}_out.png")

        generate_paint_by_numbers(filepath, output_path, num_colors)

        return send_file(output_path, mimetype='image/png')

    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
