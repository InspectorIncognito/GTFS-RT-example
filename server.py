import os

from flask import Flask, send_from_directory, current_app

app = Flask(__name__)


@app.route('/media/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(current_app.root_path, 'output')

    return send_from_directory(directory=uploads, filename=filename)


if __name__ == '__main__':
    app.run(port=5000, debug=True)