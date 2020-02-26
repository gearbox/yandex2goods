from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import send_from_directory

import xls_to_xml

SERVED_FOLDER = 'static/out'

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates'
)
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
app.config['SERVED_FOLDER'] = SERVED_FOLDER
app.secret_key = "my super duper mega secret key"


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(app.config['SERVED_FOLDER'], 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/out/<filename>')
def serve_files(filename):
    return send_from_directory(app.config['SERVED_FOLDER'], filename, mimetype='text/plain', as_attachment=True)


@app.route('/convert-xls', methods=['POST'])
def convert_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        # flash('No file part', 'warning')
        resp = jsonify({'message': 'No file part.', 'type': 'warning'})
        # resp.status_code = 400
        return resp
        # return redirect(request.path)
    file = request.files['file']
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        # flash('Не выбран ни один файл', 'warning')
        resp = jsonify({'message': 'Не выбран ни один файл.', 'type': 'warning'})
        # resp.status_code = 400
        return resp
        # return redirect(url_for('index'))
    if not xls_to_xml.allowed_filetype(file.filename):
        # flash('Данный тип файлов не поддерживается', 'danger')
        resp = jsonify({'message': 'Данный тип файлов не поддерживается.', 'type': 'danger'})
        # resp.status_code = 500
        return resp
        # return redirect(url_for('index'))
    filename = xls_to_xml.convert(file)
    if filename:
        resp = jsonify({
            'message': 'Файл успешно сконвертирован.',
            'type': 'success',
            'link': url_for('serve_files', filename=filename.name),
            'filename': filename.name
        })
        return resp
    # return redirect(url_for('serve_files', filename=filename.name))
    return render_template('converted.html', filename=filename)


if __name__ == '__main__':
    app.debug = True
    app.run()
