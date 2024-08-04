from django.db import models

class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class EmailMessage(models.Model):
    id = models.AutoField(primary_key=True)
    email_id = models.IntegerField()
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()
    attachments = models.JSONField(default=list)
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)