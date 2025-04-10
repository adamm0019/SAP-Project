import os
import re
import uuid
import logging
import bleach
from datetime import datetime
from flask import current_app, request

def sanitize_input(text):
    if text is None:
        return ""
    return bleach.clean(str(text), strip=True)

def sanitize_html(html, allowed_tags=None):
    if allowed_tags is None:
        allowed_tags = ['b', 'i', 'u', 'p', 'br', 'ul', 'ol', 'li', 'strong', 'em']
    return bleach.clean(html, tags=allowed_tags, strip=True)

def validate_username(username):
    if not username or len(username) < 3:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    return True

def validate_password(password):
    if not password or len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

def log_event(event_type, message, level='info', user_id=None):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'events.log')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    user_info = f"User ID: {user_id}" if user_id else "Anonymous"
    client_ip = request.remote_addr if request else "Unknown"

    log_entry = f"{timestamp} [{level.upper()}] {event_type}: {message} - {user_info} from {client_ip}"

    logger = logging.getLogger('app.events')

    if level.upper() == 'ERROR':
        logger.error(log_entry)
    elif level.upper() == 'WARNING':
        logger.warning(log_entry)
    else:
        logger.info(log_entry)

    with open(log_file, 'a') as f:
        f.write(log_entry + "\n")

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
        log_event('error', f"Error formatting timestamp: {e}", level='error')
        return "Invalid date"

def generate_secure_token():
    return str(uuid.uuid4())