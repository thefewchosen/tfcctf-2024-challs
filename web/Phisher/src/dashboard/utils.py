from flask_mail import Mail, Message, parseaddr
from flask import render_template_string, session, redirect, url_for
from flask_executor import Executor

import os
import random
import string


ADMIN_MAIL = os.getenv('ADMIN_MAIL', 'admin@phisher.tfc')
mail = Mail()
executor = Executor()


with open('email_templates/otp.html') as f:
    otp_template = f.read()

with open('email_templates/referral.html') as f:
    referral_template = f.read()

def generate_otp():
    return ''.join(random.choices(string.digits, k=8))

def require_login(func):
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def is_admin():
    return parseaddr(session['email'])[1] == parseaddr(ADMIN_MAIL)[1]

def send_otp(email: str, code: str):
    msg = Message(
        subject="Your Phisher Dashboard one-time code",
        recipients=[email],
        html=otp_template.replace("{{ code }}", code).replace("{{ email }}", email)
    )
    mail.send(msg)


class Referral():
    def __init__(self, email, rcpt):
        self.sender = email
        self.rcpt = rcpt
        self.template = referral_template

    def include_message(self, message):
        self.template = render_template_string(self.template, sender_email=self.sender, message=message)

    def send(self):
        msg = Message(
            subject="You were referred",
            sender=self.sender,
            recipients=[self.rcpt],
            html=self.template
        )
        mail.send(msg)


class MailEngine:
    def __init__(self):
        self.queue = []

    def send(self, sender_email, rcpt, message):
        referral = Referral(sender_email, rcpt)
        referral.include_message(message)
        self.queue.append(referral)

        self._send_emails()

    def send_bulk(self, sender_email, rcpts, message):
        self.queue.extend(Referral(sender_email, rcpt) for rcpt in rcpts)
        for referral in self.queue:
            referral.include_message(message)

        self._send_emails()

    def _send_emails(self):
        while self.queue:
            referral = self.queue.pop(0)
            referral.send()
