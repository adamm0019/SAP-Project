import os
from datetime import datetime
import sqlite3
from flask import current_app, g
from sqlalchemy import text

def get_db_connection():
    conn = sqlite3.connect(current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    conn.row_factory = sqlite3.Row
    return conn

def log_event(event_type, message, level='info'):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'events.log')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(log_file, 'a') as f:
        f.write(f"{timestamp} [{level.upper()}] {event_type}: {message}\n")

def execute_raw_query(query, params=None):
    from app import db

    try:
        with db.engine.connect() as connection:
            if params:
                result = connection.execute(text(query), params)
            else:
                result = connection.execute(text(query))

            results = [dict(row) for row in result]

            # Commit if needed
            if any(q.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')) for q in query.split(';')):
                connection.commit()

            return results
    except Exception as e:
        return {"error": str(e), "query": query}

def format_timestamp(timestamp):
    if timestamp is None:
        return ""
    try:
        if isinstance(timestamp, str):
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        else:
            dt = timestamp
        return dt.strftime('%Y-%m-%d %H:%M')
    except Exception as e:
        return "Invalid date"

def get_user_by_username(username):
    query = f"SELECT * FROM user WHERE username = '{username}' LIMIT 1"
    result = execute_raw_query(query)
    return result[0] if result and not isinstance(result, dict) and len(result) > 0 else None

def validate_password(password):
    # Very weak password validation
    return password is not None and len(password) > 0