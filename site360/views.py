from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Product, User
from .forms import ReviewForm

def url_to_product_name(url):
    return url.replace("-", " ")

def home(request):
    return render(request, 'site360/home.html', {})

def product_detail(request, productname):
    formatted_product_name = url_to_product_name(productname)
    product = get_object_or_404(Product, name=formatted_product_name)
    reviews = product.review_set.all().order_by('-date_posted') #Most recent results first

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.published_date = timezone.now()
            review.author = request.user
            review.product = product
            review.save()
    else:
        form = ReviewForm()

    return render(request, 'site360/product_detail.html', {'product_name': formatted_product_name, 'product': product, 'reviews': reviews, 'form': form})

def about_us(request):
    Product.objects.filter(full_name="").update(full_name="a")
    return render(request, 'site360/about_us.html', {})

def signup_login(request):
    return render(request, 'site360/signuplogin.html', {})

def profile_info(request, username):
    product = get_object_or_404(User, username=username)
    return render(request, 'site360/profileinfo.html', {'username': username})

def category_search(request, categoryname):
    products = Product.objects.filter(category = categoryname).order_by('-average_rating')
    return render(request, 'site360/categorysearch.html', {'category':categoryname, 'products': products})

def test_profile(request):
    return render(request, 'site360/profileinfo.html', {})
