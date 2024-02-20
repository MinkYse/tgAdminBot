from django.shortcuts import render
from django.http import Http404, HttpResponse

def index(request):
    return render(request, 'index.html')
