from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user

from .forms import CompanyProfile

from webapp.models import db, User, Currency

# Set up a Blueprint
profile_bp = Blueprint('profile_bp', __name__,
                       static_url_path='',
                       static_folder='static',
                       template_folder='templates', )


@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = CompanyProfile()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.company_name = form.company_name.data
            current_user.shop_name = form.shop_name.data
            current_user.shop_url = form.shop_url.data
            # current_user.shop_currency = form.shop_currency.data
            currency = Currency(name=form.shop_currency.data, rate=form.currency_rate.data, user_id=current_user.id)
            # current_user.shop_outlet = form.shop_outlet.data
            db.session.add(currency)
            db.session.commit()
            return redirect(url_for('profile_bp.profile'))
    else:
        form.company_name.data = current_user.company_name
        form.shop_name.data = current_user.shop_name
        form.shop_url.data = current_user.shop_url
        form.shop_currency.data = current_user.shop_currency
        # form.currency_rate.data = current_user.
        form.shop_outlet.data = current_user.shop_outlet
    return render_template('profile.html', form=form)


@profile_bp.route('/user/<user_email>')
@login_required
def user_info(user_email):
    user = User.query.filter_by(email=user_email).first_or_404()
    return render_template('user.html', user=user)
