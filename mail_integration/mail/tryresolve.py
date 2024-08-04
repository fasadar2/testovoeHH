from asgiref.sync import sync_to_async
from .models import EmailAccount, EmailMessage


@sync_to_async
def emails_by_accuont(email: str):
    return EmailAccount.objects.get(email=email)
@sync_to_async
def get_emails():
    return list(EmailMessage.objects.all())
@sync_to_async
def create_email(message, email_account):
    return EmailMessage.objects.create(
        email_id=message['email_id'],
        subject=message['subject'],
        sent_date=message['sent_date'],
        received_date=message['received_date'],
        body=message['body'],
        attachments=message['attachments'],
        email_account=email_account
    )


@sync_to_async
def is_email_in_db(email_id):
    try:
        email_message = EmailMessage.objects.filter(email_id=int(email_id))
        if email_message.email_id:
            pass
        return True
    except:
        return False
