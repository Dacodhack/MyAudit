from myaudit import db, login_manager
from myaudit.models import Users
from myaudit.forms import LoginForm, RegistrationForm
from myaudit.utils import log_action

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
@log_action
def login():
    if current_user.is_authenticated:
        return redirect(url_for('menu.dashboard'))
    login_form = LoginForm()
    register_form = RegistrationForm()
    if login_form.validate_on_submit() and 'login_submit' in request.form:
        user = Users.query.filter_by(username=login_form.username.data).first()
        if user:
            try:
                if ph.verify(user.password, login_form.password.data):
                    login_user(user)
                    flash('Login successful for {}'.format(login_form.username.data), 'success')
                    return redirect(url_for('menu.dashboard'))
                else:
                    flash('Login unsuccessful. Please check username and password.', 'danger')
            except VerifyMismatchError:
                flash('Login unsuccessful. Please check username and password.', 'danger')
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    elif register_form.validate_on_submit() and 'register_submit' in request.form:
        hashed_password = ph.hash(register_form.password.data)
        existing_admin = Users.query.filter_by(droits_generaux='admin').first()
        if existing_admin is None:
            user = Users(username=register_form.username.data, password=hashed_password, droits_generaux='admin')
            flash('Vous êtes le premier utilisateur et avez été automatiquement nommé administrateur.', 'info')
        else:
            user = Users(username=register_form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé pour {}'.format(register_form.username.data), 'success')
        return redirect(url_for('auth.login'))
    return render_template('login.html', login_form=login_form, register_form=register_form, title='Login/Registration')

@auth.route('/logout')
@log_action
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))