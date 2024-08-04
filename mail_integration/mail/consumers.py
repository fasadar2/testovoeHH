import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .mail_utils import fetch_emails
from .tryresolve import emails_by_accuont,create_email,is_email_in_db,get_emails

class MailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        email_account = await emails_by_accuont(data['email'])
        messages = fetch_emails(email_account,self)

        for i, message in enumerate(messages):
            if await is_email_in_db(message[0]['email_id']):
                continue
            email_msg = await create_email(message[0],email_account)
            await self.send(text_data=json.dumps({
                'status': 'fetching',
                'progress':message[1],
                'message': email_msg.id
            }))

        await self.send(text_data=json.dumps({
            'status': 'completed'
        }))
class MailFromDbConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
    async def receive(self,text_data):
        emails = await get_emails()
        for i,email in enumerate(emails):
            await self.send(text_data=json.dumps({
                'status':'fetching',
                'id': email.email_id,
                'subject': email.subject,
                'sent_date': str(email.sent_date),
                'received_date': str(email.received_date),
                'body': email.body,
                'attachments': email.attachments,
                'progress':100-(i+1)/len(emails)*100
            }))
        await self.send(text_data=json.dumps({
            'status': 'completed'
        }))