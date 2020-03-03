from flask import Blueprint, render_template, request, url_for, redirect

from . import forms

# Set up a Blueprint
auth_bp = Blueprint('auth_bp', __name__,
                    static_url_path='',
                    static_folder='static',
                    template_folder='templates',)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('login.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
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
