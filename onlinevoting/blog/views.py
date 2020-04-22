from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Society

def home(request):
    return render(request, 'blog/home.html')
def about(request):
    return render(request, 'blog/about.html')
