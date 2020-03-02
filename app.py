from flask import Flask, render_template, request, url_for, jsonify, redirect  # , flash
from flask import send_from_directory  # , make_response
from config import DevConfig

import xls_to_xml
import forms

# SERVED_FOLDER = 'static/out'
# app = Flask(__name__, instance_relative_config=False)
app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates',
    instance_relative_config=False
)
app.config.from_object(DevConfig())
# app.config.from_envvar('APP_CONFIG')
# app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
# app.config['SERVED_FOLDER'] = SERVED_FOLDER
# app.secret_key = "my super duper mega secret key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/out/<filename>')
def serve_files(filename):
    return send_from_directory(app.config['SERVED_FOLDER'], filename, mimetype='text/plain', as_attachment=True)


@app.route('/convert-xls', methods=['POST'])
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
            'link': url_for('serve_files', filename=filename.name),
            'filename': filename.name
        })
        return resp
    return render_template('converted.html', filename=filename)


# @login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = forms.CompanyProfile()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('profile.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = forms.SignUp(request.form)
    if request.method == 'POST':
        if signup_form.validate():
            email = request.form.get('email')
            password = request.form.get('password')
            # existing_user = User.query.filter_by(email=email).first()
            # if existing_user is None:
            #     user = User(email=email, password=generate_password_hash(password, method='sha256'))
            #     db.session.add(user)
            #     db.session.commit()
            #     login_user(user)
            #     return redirect(url_for('index'))
            # flash('A user already exists with that email address.')
            return redirect(url_for('login'))
    return render_template('signup.html', form=signup_form)


# @app.errorhandler(404)
# def not_found():
#     """Page not found."""
#     return make_response(render_template("404.html"), 404)


if __name__ == '__main__':
    app.run()
