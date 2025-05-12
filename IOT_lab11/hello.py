import os
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

BASE_DIR = 'files'
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(BASE_DIR)
    return jsonify({'files': files})

@app.route('/files/<filename>', methods=['GET'])
def read_file(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content})
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/files', methods=['POST'])
def create_file():
    if not request.json or 'filename' not in request.json or 'content' not in request.json:
        abort(400, description="Missing 'filename' or 'content'")
    filename = request.json['filename']
    content = request.json['content']
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        abort(400, description="File already exists.")
    with open(path, 'w') as f:
        f.write(content)
    return jsonify({'message': 'File created', 'filename': filename}), 201

@app.route('/files/auto', methods=['POST'])
def create_file_auto():
    if not request.json or 'content' not in request.json:
        abort(400, description="Missing 'content'")
    content = request.json['content']
    index = 1
    while True:
        filename = f"file_{index}.txt"
        path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(path):
            break
        index += 1
    with open(path, 'w') as f:
        f.write(content)
    return jsonify({'message': 'File created', 'filename': filename}), 201

@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        abort(404, description="File not found.")
    os.remove(path)
    return jsonify({'message': 'File deleted', 'filename': filename})

@app.route('/files/<filename>', methods=['PUT'])
def update_file(filename):
    if not request.json or 'content' not in request.json:
        abort(400, description="Missing 'content'")
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        abort(404, description="File not found.")
    with open(path, 'w') as f:
        f.write(request.json['content'])
    return jsonify({'message': 'File updated', 'filename': filename})

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()