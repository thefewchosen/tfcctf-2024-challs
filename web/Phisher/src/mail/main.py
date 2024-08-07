from flask import Flask, request, redirect, url_for, render_template, session, flash
from flask.json import jsonify
import os
import secrets
import gevent
import gevent.monkey
import gevent.pywsgi

from mailserver import start_mailserver
from db import User, DB, ADMIN_USER, ADMIN_PASSWORD

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(64)

PORT = int(os.getenv('MAIL_PORT', 5000))

gevent.monkey.patch_all()

maildb = DB()
maildb.add_user(User(ADMIN_USER, ADMIN_PASSWORD))


def require_login(func):
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        
        if not maildb.get_user(session['email']):
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = maildb.get_user(email)
        if user:
            flash('User already exists')
        else:
            maildb.add_user(User(email, password))
            session['email'] = email
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = maildb.get_user(email)
        if user and user.password == password:
            session['email'] = email
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')

    return render_template('login.html')

@app.route('/')
@require_login
def index():
    return render_template('index.html')

@app.route('/api/inbox', methods=['GET', 'DELETE'])
@require_login
def api():
    user_email = session['email']
    user = maildb.get_user(user_email)

    if request.method == 'DELETE':
        user.inbox.clear()
        return jsonify({'message': 'Inbox cleared'})

    return jsonify([email.__dict__() for email in user.inbox])

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    smtp_thread = gevent.spawn(start_mailserver, maildb)
    falsk_thread = gevent.pywsgi.WSGIServer(('0.0.0.0', PORT), app)
    falsk_thread.serve_forever()

    try:
        gevent.joinall([smtp_thread, falsk_thread])
    except KeyboardInterrupt:
        pass
