from flask import Blueprint, render_template, url_for, redirect

from . import forms

# Set up a Blueprint
profile_bp = Blueprint('profile_bp', __name__,
                       static_url_path='',
                       static_folder='static',
                       template_folder='templates', )


# @login_required
@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = forms.CompanyProfile()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('profile.html', form=form)
