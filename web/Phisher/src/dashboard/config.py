import os
import secrets

class Config(object):
    SECRET_KEY = secrets.token_urlsafe(64)
    MAIL_DEFAULT_SENDER = "noreply@phisher.tfc"
    MAIL_SERVER = "localhost"
    MAIL_PORT = int(os.getenv('SMTP_PORT', 10025))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    EXECUTOR_TYPE = 'thread'
    EXECUTOR_MAX_WORKERS = 5