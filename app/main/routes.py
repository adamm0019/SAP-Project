from flask import render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import MessageForm, SearchForm
from app.models import Message, User
from app.utils import log_event, sanitize_input, sanitize_html

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        message = Message(author=current_user)
        message.set_body(form.message.data)

        db.session.add(message)
        db.session.commit()

        log_event('message', f"User {current_user.username} posted a new message", user_id=current_user.id)
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
        if form.validate_on_submit():
            search_term = sanitize_input(form.search_term.data)
        else:
            search_term = sanitize_input(request.args.get('q', ''))

        if len(search_term) >= 2:
            results = Message.query.filter(
                Message.body.ilike(f"%{search_term}%")
            ).order_by(
                Message.timestamp.desc()
            ).all()

            log_event('search', f"Search performed for term: {search_term}",
                      user_id=current_user.id if current_user.is_authenticated else None)

    return render_template('search.html', title='Search', form=form,
                           results=results, search_term=search_term)

@bp.route('/user/<username>')
def user_profile(username):
    username = sanitize_input(username)
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    messages = user.messages.order_by(Message.timestamp.desc()).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('user_profile.html', user=user, messages=messages)

@bp.route('/message/<int:id>')
def message(id):
    try:
        message_id = int(id)
        message = Message.query.get_or_404(message_id)
        return render_template('message.html', message=message)
    except ValueError:
        abort(404)
    except Exception as e:
        log_event('error', f"Error accessing message {id}: {str(e)}", level='error')
        abort(500)

@bp.route('/edit_message/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_message(id):
    try:
        message_id = int(id)
        message = Message.query.get_or_404(message_id)

        if message.author != current_user:
            log_event('security', f"User {current_user.username} attempted to edit message {id} belonging to {message.author.username}",
                      user_id=current_user.id, level='warning')
            flash('You can only edit your own messages.')
            return redirect(url_for('main.index'))

        form = MessageForm()

        if form.validate_on_submit():
            message.set_body(form.message.data)
            db.session.commit()

            log_event('message', f"User {current_user.username} edited message {id}", user_id=current_user.id)
            flash('Your message has been updated.')
            return redirect(url_for('main.message', id=message.id))
        elif request.method == 'GET':
            form.message.data = message.body

        return render_template('edit_message.html', form=form)
    except ValueError:
        abort(404)
    except Exception as e:
        log_event('error', f"Error editing message {id}: {str(e)}", level='error')
        abort(500)

@bp.route('/delete_message/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    try:
        message_id = int(id)
        message = Message.query.get_or_404(message_id)

        if message.author != current_user:
            log_event('security', f"User {current_user.username} attempted to delete message {id} belonging to {message.author.username}",
                      user_id=current_user.id, level='warning')
            flash('You can only delete your own messages.')
            return redirect(url_for('main.index'))

        db.session.delete(message)
        db.session.commit()

        log_event('message', f"User {current_user.username} deleted message {id}", user_id=current_user.id)
        flash('Your message has been deleted.')
        return redirect(url_for('main.index'))
    except ValueError:
        abort(404)
    except Exception as e:
        log_event('error', f"Error deleting message {id}: {str(e)}", level='error')
        abort(500)