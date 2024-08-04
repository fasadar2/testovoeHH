from asgiref.sync import sync_to_async
from django.shortcuts import render
from .models import EmailMessage

def message_list(request):
    return render(request, 'message_list.html' )