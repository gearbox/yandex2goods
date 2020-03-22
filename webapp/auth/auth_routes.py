from flask import Blueprint, render_template, request, url_for, redirect  # , make_response
from flask_login import login_required, logout_user, current_user, login_user
from datetime import datetime as dt
# from flask import current_app as app
from webapp.models import db, User  # , Currency, Outlet, Category
from .forms import Login, SignUp
from webapp import login_manager

# Set up a Blueprint
auth_bp = Blueprint('auth_bp', __name__,
                    static_url_path='',
                    static_folder='static',
                    template_folder='templates',
                    )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))  # Bypass if user is logged in
    login_form = Login()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()  # Validate Login Attempt
            if user and user.check_password(password=password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main_bp.index'))
                # return redirect(url_for('success'))
    return render_template('login.html', form=login_form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUp()
    if request.method == 'POST':
        print('POST')
        print(request.form)
        print(signup_form.errors)
        if signup_form.validate_on_submit():
            print('Valid, continue')
            email = signup_form.email.data
            password = signup_form.password.data
            existing_user = User.query.filter_by(email=email).first()  # Check if user exists
            # existing_user = User.query.filter(User.email == email).first()

            if existing_user is None:
                print('User is None, continue')
                # user = User(email=email,
                #             created_on=dt.now())
                user = User()
                user.email = email
                user.created_on = dt.now()
                user.set_password(password)
                db.session.add(user)
                db.session.commit()  # Create new user
                login_user(user)  # Log in as newly created user
                return redirect(url_for('profile_bp.profile'))
            # return make_response(f'User with email: {email} already exists!')

    return render_template('signup.html', form=signup_form)


# TODO: Limit access to Admin users only
@auth_bp.route('/users', methods=['GET'])
@login_required
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@auth_bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page. You must be logged in to view that page."""
    return redirect(url_for('auth_bp.login'))
