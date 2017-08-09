from django.shortcuts import render

from .models import *

def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasklist/home.html', {'tasks': tasks})
