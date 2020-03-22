from flask import Blueprint, redirect, url_for, request
from flask import current_app as app
from webapp.models import db, User, Currency, Outlet, Category
from flask_login import logout_user, current_user, login_user
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import helpers, expose
from flask_admin.contrib.sqla import ModelView
from ..auth.forms import Login, SignUp

# Set up a Blueprint
admin_bp = Blueprint('admin_bp', __name__,
                     static_url_path='',
                     static_folder='static',
                     template_folder='templates',
                     )

# admin = Admin(
#     name='Yandex2Goods Admin',
#     template_mode='bootstrap3',
#     # index_view=MyAdminIndexView(),
#     # base_template='admin_indx.html',
# )
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Currency, db.session))
# admin.add_view(ModelView(Outlet, db.session))
# admin.add_view(ModelView(Category, db.session))
# admin.init_app(app)


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('../login', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = Login(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('../signup', methods=('GET', 'POST'))
    def register_view(self):
        form = SignUp(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


# Create admin
# admin = Admin(app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='my_master.html')
admin = Admin(
    # admin_bp,
    name='Yandex2Goods Admin',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView(),
    # base_template='admin_indx.html',
)

# Add view
admin.add_view(MyModelView(User, db.session))
# admin.add_view(ModelView(User, db.session))
admin.add_view(MyModelView(Currency, db.session))
admin.add_view(MyModelView(Outlet, db.session))
admin.add_view(MyModelView(Category, db.session))
admin.init_app(app)
