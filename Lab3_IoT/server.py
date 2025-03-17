import io
from flask import Flask, send_file, jsonify
import os.path

app = Flask(__name__)

@app.route('/firmware.bin')
def firm():
    with open(".pio\\build\\esp-wrover-kit\\firmware.bin", 'rb') as bites:
        print(bites)
        return send_file(
                     io.BytesIO(bites.read()),
                     mimetype='application/octet-stream'
               )

@app.route("/version")
def version():
    # Citim fișierul version.h pentru a obține informațiile despre versiune
    with open("versioning", 'r') as f:
        version_info = f.readline()
        print(version_info)
        return version_info

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('ca_cert.pem', 'ca_key.pem'), debug=True)