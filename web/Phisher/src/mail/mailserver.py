import os
import smtpd
import asyncore
from email.parser import BytesParser
from email.policy import default

from db import Email, DB

SMTP_PORT = int(os.getenv('SMTP_PORT', 10025))


class MailServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, database: DB):
        super().__init__(localaddr, remoteaddr)
        self.database = database

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        msg = BytesParser(policy=default).parsebytes(data)
        processed_email = Email(
            from_=mailfrom,
            to=rcpttos[0],
            subject=msg['Subject'],
            body=msg.get_body().get_payload()
        )

        self.database.add_email(processed_email)
        return

def start_mailserver(maildb: DB):
    server = MailServer(('0.0.0.0', SMTP_PORT), None, maildb)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass