from django.shortcuts import render, get_object_or_404
from .models import Product

def url_to_product_name(url):
    return url.replace("-", " ")

def home(request):
    return render(request, 'site360/home.html', {})

def product_detail(request, productname):
    formatted_product_name = url_to_product_name(productname)
    product = get_object_or_404(Product, name=formatted_product_name)
    return render(request, 'site360/post_detail.html', {'product_name': formatted_product_name})

def about_us(request):
    return render(request, 'site360/about_us.html', {})

def signup_login(request):
    return render(request, 'site360/signuplogin.html', {})
