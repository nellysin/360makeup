from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.utils import timezone
from .models import Product, Favorite, Rating, Profile
from .forms import ReviewForm, ProfilePictureForm
import decimal

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
            break

    if not correct_product:
        raise Http404('Product does not exist')

    is_product_favorite = False
    favorite_users = Favorite.objects.filter(product=correct_product)
    # If the current user has not yet favorited this product:
    if request.user.is_authenticated:
        current_user_favorite = favorite_users.filter(user=request.user)
        if current_user_favorite.count() == 0:
            is_product_favorite = False
            if request.GET.get('favoritebutton'):
                favorite = Favorite()
                favorite.product = correct_product
                favorite.user = request.user
                favorite.save()
                current_url = request.get_full_path().split("?")[0]
                return redirect(current_url)
        else:
            is_product_favorite = True
            if request.GET.get('removefavoritebutton'):
                current_user_favorite.delete()
                current_url = request.get_full_path().split("?")[0]
                return redirect(current_url)

    # Calculate and store ratings
    # *WEEPS* FORGIVE ME
    current_url = request.get_full_path()
    rated_users = Rating.objects.filter(product=correct_product) # Ratings of users who rated this product
    rated_users_list = {rating.reviewer: int(rating.rating) for rating in rated_users}
    print (rated_users_list)
    current_user_ratings = rated_users.filter(reviewer=request.user).all()
    if "?ratebutton=Give" in current_url:
        current_split_url = current_url.split("?ratebutton=Give+this+product+")
        current_rating = current_split_url[1][0]
        if current_user_ratings.count() == 0: # User has rated product for the first time
            rating = Rating()
            rating.product = correct_product
            rating.reviewer = request.user
            rating.rating = current_rating
            correct_product.number_of_ratings += 1
            correct_product.save()
        else:
            rating = current_user_ratings[0]
            rating.rating = current_rating

        rating.save()

        #average_rating = models.FloatField()
        #number_of_ratings = models.IntegerField()

        rating_sum = 0
        # Recalculate product rating
        for product_rating in rated_users:
            rating_sum += product_rating.rating
        average_rating = rating_sum/correct_product.number_of_ratings
        correct_product.average_rating = round(decimal.Decimal(average_rating), 1)
        correct_product.save()

        return redirect(current_split_url[0])

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
            current_url = request.get_full_path()
            return redirect(current_url)
    else:
        form = ReviewForm()

    return render(request, 'site360/product_detail.html', {'product_name': correct_product.name, 'product': correct_product, 'reviews': reviews, 'form': form, 'review_count': review_count, 'is_product_favorite': is_product_favorite, 'rated_users_list': rated_users_list})

def about_us(request):
    return render(request, 'site360/about_us.html', {})

def signup_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        user_profile = Profile.objects.filter(user=user).all()
        if user_profile.count() == 0:
            profile = Profile()
            profile.user = user
            profile.save()
    else:
        pass # Return an 'invalid login' error message.
    return render(request, 'site360/signuplogin.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'site360/signup.html', {'form': form})

def profile_info(request, username):
    user = get_object_or_404(User, username=username)
    #profile = Profile.objects.filter(user=user)[0]
    # TO DO: IF USER TRIES TO GET PROFILE, CREATE NEW PROFILE
    favorites = Favorite.objects.filter(user=user).all()

    picture_url = user.profile.picture_url

    # THIS DOESN'T WORK
    if request.method == "POST":
        form = ProfilePictureForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            picture_url = form_data.picture_url
            user.profile.picture_url = picture_url
            user.save()
            current_url = request.get_full_path()
            return redirect(current_url)
    else:
        form = ProfilePictureForm()

    return render(request, 'site360/profileinfo.html', {'username': username, 'favorites': favorites, 'form': form, 'picture_url': picture_url})

def category_search(request, categoryname):
    products = Product.objects.filter(category = categoryname).order_by('-average_rating')
    return render(request, 'site360/categorysearch.html', {'category':categoryname, 'products': products})

def tutorials(request):
    return render(request, 'site360/tutorials.html', {})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
