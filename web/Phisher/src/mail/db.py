from typing import List
import os
import secrets

from bot import bot_visit

ADMIN_USER = os.getenv('ADMIN_USER', 'admin@phisher.tfc')
ADMIN_PASSWORD = secrets.token_urlsafe(16)

class User:
    def __init__(self, email, password):
        self.email: str = email
        self.password: str = password
        self.inbox: List[Email] = []

    def __repr__(self) -> str:
        return f'{self.email}'

class Email:
    def __init__(self, from_, to, subject, body):
        self.from_: str = from_
        self.to: str = to
        self.subject: str = subject
        self.body: str = body

    def __dict__(self):
        return {
            'from': self.from_,
            'to': self.to,
            'subject': self.subject,
            'body': self.body
        }

    def __repr__(self):
        return f'{self.subject}'

class DB:
    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User):
        self.users.append(user)

    def get_user(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user

    def add_email(self, email: Email):
        for user in self.users:
            if user.email == email.to:
                user.inbox.append(email)

                if email.to == ADMIN_USER:
                    bot_visit(ADMIN_USER, ADMIN_PASSWORD)

    def get_emails(self, email: str) -> List[Email]:
        for user in self.users:
            if user.email == email:
                return user.inbox

    def __repr__(self):
        return f'{self.users}'
