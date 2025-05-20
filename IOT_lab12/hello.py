import os
import random
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

FILES_DIR = 'files'
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(FILES_DIR)
    return jsonify({'files': files})

@app.route('/files/<filename>', methods=['GET'])
def read_file(filename):
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'File not found'}), 404
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return jsonify({'filename': filename, 'content': content})

@app.route('/files', methods=['POST'])
def create_file():
    if not request.json or 'filename' not in request.json or 'content' not in request.json:
        abort(400, description="Missing 'filename' or 'content'")
    filename = request.json['filename']
    content = request.json['content']
    path = os.path.join(FILES_DIR, filename)
    if os.path.exists(path):
        abort(400, description="File already exists.")
    with open(path, 'w', encoding='utf-8') as f:
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
        path = os.path.join(FILES_DIR, filename)
        if not os.path.exists(path):
            break
        index += 1
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return jsonify({'message': 'File created', 'filename': filename}), 201

@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        abort(404, description="File not found.")
    os.remove(path)
    return jsonify({'message': 'File deleted', 'filename': filename})

@app.route('/files/<filename>', methods=['PUT'])
def update_file(filename):
    if not request.json or 'content' not in request.json:
        abort(400, description="Missing 'content'")
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        abort(404, description="File not found.")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(request.json['content'])
    return jsonify({'message': 'File updated', 'filename': filename})

SENSOR_CONFIG_DIR = 'sensors'
if not os.path.exists(SENSOR_CONFIG_DIR):
    os.makedirs(SENSOR_CONFIG_DIR)

@app.route('/sensor/<sensor_id>', methods=['GET'])
def get_sensor_value(sensor_id):
    value = round(random.uniform(10.0, 30.0), 2)  # temperatură simulată
    return jsonify({
        "sensor_id": sensor_id,
        "value": value,
        "unit": "°C"
    })

@app.route('/sensor/<sensor_id>', methods=['POST'])
def create_sensor_config(sensor_id):
    config_path = os.path.join(SENSOR_CONFIG_DIR, f"{sensor_id}_config.txt")
    if os.path.exists(config_path):
        return jsonify({
            "error": "Config file already exists.",
            "code": 409
        }), 409

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write("scale=1.0\nunit=°C")

    return jsonify({
        "message": "Config file created.",
        "file": f"{sensor_id}_config.txt"
    }), 201

@app.route('/sensor/<sensor_id>/<filename>', methods=['PUT'])
def update_sensor_config(sensor_id, filename):
    config_path = os.path.join(SENSOR_CONFIG_DIR, filename)
    if not os.path.exists(config_path):
        return jsonify({
            "error": "Cannot update. Config file does not exist.",
            "code": 409
        }), 409

    if not request.json or 'content' not in request.json:
        abort(400, description="Missing 'content'")

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(request.json['content'])

    return jsonify({
        "message": "Config file updated.",
        "file": filename
    })

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)