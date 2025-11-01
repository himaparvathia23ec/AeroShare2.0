from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import random
import string

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'shared_files')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

share_codes = {}  # {code: filename}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Generate a random 6-character share code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    share_codes[code] = filename

    return jsonify({"code": code})

@app.route('/download', methods=['POST'])
def download_file():
    data = request.get_json()
    code = data.get('code')

    if code in share_codes:
        filename = share_codes[code]
        return jsonify({"filename": filename})
    else:
        return jsonify({"error": "Invalid code"}), 404

@app.route('/get_file/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
