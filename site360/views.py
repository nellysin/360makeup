from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Product, User
from .forms import ReviewForm

def url_to_product_name(url):
    return url.replace("-", " ")

def home(request):
    return render(request, 'site360/home.html', {})

def product_detail(request, productname):
    all_products = Product.objects.all()
    correct_product = 0
    for product in all_products:
        if product.name_to_url() == productname:
            correct_product = product
    #correct_product = get_object_or_404(Product, name=formatted_product_name)

    if not correct_product:
        raise Http404("Product does not exist")

    reviews = correct_product.review_set.all().order_by('-date_posted') #Most recent reviews first
    review_count = reviews.count()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.published_date = timezone.now()
            review.author = request.user
            review.product = correct_product
            review.save()
            reviews = correct_product.review_set.all().order_by('-date_posted') #Most recent reviews first
            review_count = reviews.count()
    else:
        form = ReviewForm()

    return render(request, 'site360/product_detail.html', {'product_name': correct_product.name, 'product': correct_product, 'reviews': reviews, 'form': form, 'review_count': review_count})

def about_us(request):
    return render(request, 'site360/about_us.html', {})

def signup_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        pass # Return an 'invalid login' error message.
    return render(request, 'site360/signuplogin.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'site360/signup.html', {'form': form})

def profile_info(request, username):
    product = get_object_or_404(User, username=username)
    return render(request, 'site360/profileinfo.html', {'username': username})

def category_search(request, categoryname):
    products = Product.objects.filter(category = categoryname).order_by('-average_rating')
    return render(request, 'site360/categorysearch.html', {'category':categoryname, 'products': products})

def test_profile(request):
    return render(request, 'site360/profileinfo.html', {})
