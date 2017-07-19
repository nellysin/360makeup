from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    return render(request, 'site360/home.html', {})

def product_detail(request, productname):
    product = get_object_or_404(Product, name=productname)
    return render(request, 'site360/post_detail.html', {'product_name': productname})
