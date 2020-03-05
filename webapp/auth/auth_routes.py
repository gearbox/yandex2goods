from flask import Blueprint, render_template, request, url_for, redirect, make_response
from datetime import datetime as dt
# from flask import current_app as app
from .models import db, User
from . import forms
from . import auth

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
        print('POST')
        if signup_form.validate():
            print('Valid!')
        else:
            print('Not Valid!')
        email = request.form.get('email')
        print('*EMAIL: ', email)
        password = request.form.get('password')
        password = auth.hash_password(password)
        if email and password:
            existing_user = User.query.filter(User.email == email).first()
            # existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return make_response(f'User with email: {email} already exists!')
            new_user = User(username=None,
                            email=email,
                            password=password,
                            bio=None,
                            created=dt.now(),
                            active=False,
                            active_since=None,
                            admin=False)
            db.session.add(new_user)
            db.session.commit()
        # if existing_user is None:
        #     user = User(email=email, password=generate_password_hash(password, method='sha256'))
        #     db.session.add(user)
        #     db.session.commit()
        #     login_user(user)
        #     return redirect(url_for('index'))
        # flash('A user already exists with that email address.')
        # return redirect(url_for('login'))
            return make_response(f'{new_user} successfully created!')
        print('GET')
    return render_template('signup.html', form=signup_form)


@auth_bp.route('/users', methods=['GET'])
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)
