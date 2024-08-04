import imaplib
import email
import json
from email.header import decode_header
import datetime
from .models import EmailMessage

def fetch_emails(email_account,consumer):
    imap_server = 'imap.yandex.ru'
    email_user = email_account.email
    email_pass = email_account.password

    server = imaplib.IMAP4_SSL(imap_server)
    server.login(email_user, email_pass)
    server.select("inbox")

    status, messages = server.search(None, "ALL")
    email_ids = messages[0].split()

    fetched_emails = []

    for i,email_id in enumerate(email_ids):
        status, msg_data = server.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        if "Subject" in msg.keys():
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
        sent_date = email.utils.parsedate_to_datetime(msg["Date"])
        received_date = datetime.datetime.now()

        body = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
                elif content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()
        if (i+1) == len(email_ids):
            server.logout()
        yield {
            "email_id":int(email_id),
            "subject": subject,
            "sent_date": sent_date,
            "received_date": received_date,
            "body": body,
            "attachments": attachments,
        },(i + 1) / len(email_ids) * 100
