from .models import Client

TOKEN = '6644534760:AAGNW1Wkjw5kw9fDjn68WdHZAvYKj50sPWM'

name = 'Иван'

client = Client()
client.username = name
client.save()