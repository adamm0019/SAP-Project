from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from sqlalchemy import text
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        raw_query = f"SELECT * FROM user WHERE username = '{username}'"

        try:
            import sqlite3
            conn = sqlite3.connect('instance/app.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(raw_query)
            user_data = cursor.fetchone()

            if user_data:
                user_dict = dict(user_data)
                print(f"Found user: {user_dict}")

                user = User.query.get(user_dict['id'])
                if user:
                    login_user(user, remember=form.remember_me.data)
                    next_page = request.args.get('next')
                    if not next_page or not next_page.startswith('/'):
                        next_page = url_for('main.index')
                    return redirect(next_page)

            flash(f'Invalid username or password')

        except Exception as e:
            flash(f'Login error: {str(e)}')
            print(f"SQL Error: {str(e)}")
            print(f"Query was: {raw_query}")

        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'User {form.username.data} registered with password length {len(form.password.data)}!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)