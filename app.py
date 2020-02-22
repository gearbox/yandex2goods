from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import send_from_directory

import xls_to_xml

SERVED_FOLDER = project_dir_path = Path(__file__).parent / '/static/out'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
app.config['SERVED_FOLDER'] = SERVED_FOLDER
app.secret_key = "my super duper mega secret key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/out/<filename>')
def serve_files(filename):
    return send_from_directory(app.config['SERVED_FOLDER'], filename)


@app.route('/convert-xls', methods=['POST'])
def convert_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.host_url)
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.host_url)
    filename = xls_to_xml.convert(file)
    return redirect(url_for('serve_files', filename=filename.name))


if __name__ == '__main__':
    app.debug = True
    app.run()
