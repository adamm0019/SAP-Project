from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.utils import log_event, sanitize_input

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = sanitize_input(form.username.data)
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            log_event('auth', f"Failed login attempt for {username}", level='warning')
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        log_event('auth', f"User {username} logged in", user_id=user.id)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        log_event('auth', f"User {current_user.username} logged out", user_id=current_user.id)

    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = sanitize_input(form.username.data)
        email = sanitize_input(form.email.data)

        user = User(username=username, email=email)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        log_event('auth', f"New user registered: {username}", level='info')
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)