from django.shortcuts import render
from django.http import HttpResponse
from .models import Society

def home(request):
    context = {
     'societies' : Society.objects.all()
    }
    return render(request, 'blog/home.html', context)
def about(request):
    return render(request, 'blog/about.html')
