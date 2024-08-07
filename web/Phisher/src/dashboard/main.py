import os
from flask import Flask, request, redirect, url_for, render_template, session, flash

from utils import require_login, is_admin, generate_otp, send_otp, mail, executor, MailEngine

PORT = int(os.getenv('DASHBOARD_PORT', 3000))
app = Flask(__name__)
app.config.from_object('config.Config')

mail.init_app(app)
executor.init_app(app)
mail_engine = MailEngine()

user_otps = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']

        # Generate and send otp
        code = generate_otp()
        executor.submit(send_otp, email, code)
        user_otps[email] = code

        # Redirect to verify page
        session['pending_email'] = email
        return redirect(url_for('verify_code'))

    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        email = session.get('pending_email')
        code = request.form['code']

        if email in user_otps and user_otps[email] == code:
            session['email'] = email
            session.pop('pending_email', None)
            user_otps.pop(email)

            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            # Invalidate the code
            user_otps.pop(email, None)

            flash('Invalid code. Please try again.')
            return redirect(url_for('login'))

    return render_template('verify.html')

@app.route('/')
@require_login
def index():
    return render_template('index.html', username=session['email'])

@app.route('/refer', methods=['GET', 'POST'])
@require_login
def refer():
    if request.method == 'POST':
        sender = session['email']
        message = request.form['message']
        emails = request.form['emails']

        if ',' in emails:
            if is_admin():
                emails = emails.split(',')
                mail_engine.send_bulk(sender, emails, message)
            else:
                flash('Only admin can send bulk referrals.')
                return redirect(url_for('refer'))
        else:
            mail_engine.send(sender, emails, message)

        flash('Referral sent successfully.')
        return redirect(url_for('index'))

    return render_template('refer.html')

@app.route('/logout')
def logout():
    session.pop('email', None)

    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
