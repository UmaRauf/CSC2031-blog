from flask import Blueprint, render_template, redirect, url_for, flash,session
from users.forms import RegisterForm, LoginForm, PasswordForm
from models import User
from app import db
from flask_login import login_user, logout_user,current_user,login_required
from markupsafe import Markup



users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.verify_password(form.password.data) and user.verify_pin(form.pin.data):
            login_user(user)
            return redirect(url_for('blog.blog'))
        else:
            flash('Invalid username, password, or PIN')

    # Handling authentication attempts
    if 'authentication_attempts' not in session:
        session['authentication_attempts'] = 0

    session['authentication_attempts'] += 1

    if session['authentication_attempts'] >= 3:
        flash(Markup('Number of incorrect login attempts exceeded. Please click <a href="/reset">here</a> to reset.'))
        return render_template('users/login.html')

    flash('Please check your login details and try again')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/account')
@login_required
def account():
    return render_template('users/account.html')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists')
            return render_template('users/register.html', form=form)

        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username

        return redirect(url_for('users.setup_2fa'))

    return render_template('users/register.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users_blueprint.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordForm()

    if form.validate_on_submit():
        # Check if current password entered by the user matches the current password stored for the user in the database
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect')
            return render_template('users/update_password.html', form=form)

        # Check if new password entered by the user is the same as the current password stored for the user in the database
        if current_user.check_password(form.new_password.data):
            flash('New password must be different from the current password')
            return render_template('users/update_password.html', form=form)

        current_user.password = form.new_password.data
        db.session.commit()
        flash('Password changed successfully')

        return redirect(url_for('users.account'))

    return render_template('users/update_password.html', form=form)

@users_blueprint.route('/setup_2fa')
def setup_2fa():
    if 'username' not in session:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(username=session['username']).first()

    if not user:
        return redirect(url_for('main.index'))

    del session['username']

    # Assuming you have a method named get_2fa_uri in your User model
    uri = user.get_2fa_uri()

    return render_template('users/setup_2fa.html', username=user.username, uri=uri), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }

@users_blueprint.route('/reset')
def reset():
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))




