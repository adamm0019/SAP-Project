from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import text
from app import db
from app.main import bp
from app.main.forms import MessageForm, SearchForm
from app.models import Message, User

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        message = Message(body=form.message.data, author=current_user)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been posted!')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(Message.timestamp.desc()).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('index.html', title='Home', form=form, messages=messages)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = []
    search_term = ""

    if form.validate_on_submit() or request.args.get('q'):
        search_term = form.search_term.data if form.validate_on_submit() else request.args.get('q', '')

        query = f"SELECT id, body, timestamp, user_id FROM message WHERE body LIKE '%{search_term}%'"

        try:
            import sqlite3
            conn = sqlite3.connect('instance/app.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                row_dict = dict(row)
                try:
                    user = User.query.get(row_dict['user_id'])
                    row_dict['author'] = {'username': user.username if user else 'Unknown'}
                except:
                    row_dict['author'] = {'username': f"User #{row_dict['user_id']}"}

                results.append(row_dict)

        except Exception as e:
            flash(f'Search error: {str(e)}')
            print(f"SQL Error: {str(e)}")
            print(f"Query was: {query}")

    if request.args.get('q') and not form.validate_on_submit():
        search_term = request.args.get('q')

    return render_template('search.html', title='Search', form=form,
                           results=results, search_term=search_term)

@bp.route('/user/<username>')
def user_profile(username):
    try:
        import sqlite3
        conn = sqlite3.connect('instance/app.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = f"SELECT * FROM user WHERE username = '{username}'"
        print(f"Executing query: {query}")

        cursor.execute(query)
        user_data = cursor.fetchone()

        if not user_data:
            flash(f'User {username} not found!')
            return redirect(url_for('main.index'))

        user_dict = dict(user_data)
        print(f"Found user: {user_dict}")

        cursor.execute(f"SELECT * FROM message WHERE user_id = {user_dict['id']} ORDER BY timestamp DESC")
        messages_data = cursor.fetchall()

        messages = []
        for row in messages_data:
            message_dict = dict(row)
            messages.append(message_dict)

        return render_template('user_profile_raw.html', user=user_dict, messages=messages)

    except Exception as e:
        flash(f'Error: {str(e)}')
        print(f"Profile error: {str(e)}")
        return redirect(url_for('main.index'))

@bp.route('/message/<int:id>')
def message(id):
    message = Message.query.get_or_404(id)
    return render_template('message.html', message=message)

@bp.route('/edit_message/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_message(id):
    message = Message.query.get_or_404(id)

    if message.author != current_user:
        flash('You cannot edit this message!')
        return redirect(url_for('main.index'))

    form = MessageForm()

    if form.validate_on_submit():
        message.body = form.message.data
        db.session.commit()
        flash('Your message has been updated.')
        return redirect(url_for('main.message', id=message.id))
    elif request.method == 'GET':
        form.message.data = message.body

    return render_template('edit_message.html', form=form)

@bp.route('/delete_message/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    message = Message.query.get_or_404(id)

    if message.author != current_user:
        flash('You cannot delete this message!')
        return redirect(url_for('main.index'))

    db.session.delete(message)
    db.session.commit()
    flash('Your message has been deleted.')
    return redirect(url_for('main.index'))