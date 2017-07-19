from django.shortcuts import render

def post_list(request):
    return render(request, 'site360/home.html', {})
