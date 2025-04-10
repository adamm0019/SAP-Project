import os
import secrets
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    BCRYPT_LOG_ROUNDS = 12

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/messageboard.log')

    CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' https://cdn.jsdelivr.net",
        'style-src': "'self' https://cdn.jsdelivr.net",
        'img-src': "'self' data:",
        'font-src': "'self'",
        'frame-src': "'none'",
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False