"""Routes for main pages"""
from flask import Blueprint, render_template, send_from_directory, request, jsonify, url_for
from flask import current_app as app
from flask_login import login_required

import xls_to_xml


# Set up a Blueprint
main_bp = Blueprint('main_bp', __name__,
                    static_url_path='',
                    static_folder='static',
                    template_folder='templates',)


@main_bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@main_bp.route('/out/<filename>')
def serve_files(filename):
    return send_from_directory(app.config['SERVED_FOLDER'], filename, mimetype='text/plain', as_attachment=True)


@main_bp.route('/convert', methods=['POST'])
def convert_file():
    """
    JSON response types: success (green), info (blue), warning (yellow), danger (red)
    :return:
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part.', 'type': 'warning'})
        # resp.status_code = 400
        return resp
    file = request.files['file']
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        resp = jsonify({'message': 'Не выбран ни один файл.', 'type': 'warning'})
        # resp.status_code = 400
        return resp
    if not xls_to_xml.allowed_filetype(file.filename):
        resp = jsonify({'message': 'Данный тип файлов не поддерживается.', 'type': 'danger'})
        return resp
    filename = xls_to_xml.convert(file)
    if filename:
        resp = jsonify({
            'message': 'Файл успешно сконвертирован.',
            'type': 'success',
            'link': url_for('main_bp.serve_files', filename=filename.name),
            'filename': filename.name
        })
        return resp
    return render_template('converted.html', filename=filename)
