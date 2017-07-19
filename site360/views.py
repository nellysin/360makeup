from django.shortcuts import render

def home(request):
    return render(request, 'site360/home.html', {})
