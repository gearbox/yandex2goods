from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required

from .forms import CompanyProfile

# Set up a Blueprint
profile_bp = Blueprint('profile_bp', __name__,
                       static_url_path='',
                       static_folder='static',
                       template_folder='templates', )


@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = CompanyProfile()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('profile.html', form=form)
