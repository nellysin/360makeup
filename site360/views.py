from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.utils import timezone
from .models import Product, Favorite, Rating, Profile, Dupe
from .forms import ReviewForm, ProfilePictureForm
import decimal

# views.py is the code of the page

def home(request):
    # The home page
    return render(request, 'site360/home.html', {})

def product_detail(request, productname):

    # Get product object requested by url
    all_products = Product.objects.all()
    correct_product = 0
    for product in all_products:
        if product.name_to_url() == productname:
            correct_product = product
            break

    # Raise error if the product requested doesn't exist
    if not correct_product:
        raise Http404('Product does not exist')

    # Handle user marking product as their favorite
    is_product_favorite = False
    favorite_users = Favorite.objects.filter(product=correct_product)

    # If the current user has not yet favorited this product:
    if request.user.is_authenticated:
        current_user_favorite = favorite_users.filter(user=request.user)
        if current_user_favorite.count() == 0:
            is_product_favorite = False

            # If the user has pressed the favorite button:
            if request.GET.get('favoritebutton'):

                # Create a new favorite object
                favorite = Favorite()

                # Fill in its details
                favorite.product = correct_product
                favorite.user = request.user
                favorite.save()

                # Reload the page so the page knows the user has marked the product
                # as a favorite
                current_url = request.get_full_path().split("?")[0]
                return redirect(current_url)

        else: # If the product is already a favorite:
            is_product_favorite = True

            # If the user has pressed the remove button:
            if request.GET.get('removefavoritebutton'):

                # Delete the favorite object
                current_user_favorite.delete()

                # Reload the page so the script doesn't try to remove the product twice
                current_url = request.get_full_path().split("?")[0]
                return redirect(current_url)

    # Calculate and store ratings
    # *WEEPS* FORGIVE ME

    # Ratings of users who rated this product
    rated_users = Rating.objects.filter(product=correct_product)
    # The number of users who have rated this product
    ratings_count = rated_users.count()
    # Dictionary associating each user who has rated the product with the rating they gave it
    rated_users_list = {rating.reviewer: int(rating.rating) for rating in rated_users}

    # Recalculate product rating
    correct_product.number_of_ratings = ratings_count

    # If people have rated this product so far:
    if correct_product.number_of_ratings:

        # Take the average of all submitted reviews
        rating_sum = 0
        for product_rating in rated_users:
            rating_sum += int(product_rating.rating)
        average_rating = float(rating_sum)/float(correct_product.number_of_ratings)
        correct_product.average_rating = round(decimal.Decimal(average_rating), 1)

    # If no one has rated this product yet:
    else:
        # Set the average rating to zero
        correct_product.average_rating = 0

    # Update the current product's rating in the database
    correct_product.save()

    # If the user is logged in:
    if request.user.is_authenticated:
        # Get the rating the user gave this product
        current_user_ratings = rated_users.filter(reviewer=request.user).all()

        # Get the page's current URL
        current_url = request.get_full_path()
        # If the user pressed the "Give this product [x] stars" button (thus rating it):
        if "?ratebutton=Give" in current_url:
            # Find out from the button how many stars the user gave this product
            current_split_url = current_url.split("?ratebutton=Give+this+product+")
            current_rating = current_split_url[1][0]

            # If this is the user's first time rating the product:
            if current_user_ratings.count() == 0:

                # Create a new Rating object
                rating = Rating()

                #Fill it in with the correct information
                rating.product = correct_product
                rating.reviewer = request.user
                rating.rating = current_rating
                correct_product.save()

            # If the user has rated this product before:
            else:

                # Access the user's previous rating object
                rating = current_user_ratings[0]
                # Set the rating value to the new rating
                rating.rating = current_rating

            # Save the rating object, be it new or updated, to the database
            rating.save()

            # Recalculate product rating
            rating_sum = 0
            for product_rating in rated_users:
                rating_sum += int(product_rating.rating)
            # Add in the most recent ratings
            rating_sum += int(current_rating)
            average_rating = float(rating_sum)/float(correct_product.number_of_ratings+1)

            # Update the product's average rating with the new value
            correct_product.average_rating = round(decimal.Decimal(average_rating), 1)
            # Recalculate the number of users who have rated this product
            rated_users = Rating.objects.filter(product=correct_product)
            ratings_count = rated_users.count()
            # Update the product with the new information
            correct_product.number_of_ratings = ratings_count
            correct_product.save()

            # Redirect the user so multiple review objects are not created
            return redirect(current_split_url[0])

        # If the user didn't just rate the product:

        # If the user has rated the product before:
        if current_user_ratings.count():
            # Get the rating they previously gave the product
            current_user_rating = int(current_user_ratings[0].rating)

        # If the user hasn't rated the product, or if they aren't logged in:
        # automatically set their rating to 0
        else:
            current_user_rating = 0
    else:
        current_user_rating = 0

    # Get the formatted list of places to buy online
    buy_online = correct_product.buy_online_to_list()

    # Get dupes
    dupes = correct_product.dupe_set.all().order_by('name')

    # Get all reviews and the total number of reviews
    reviews = correct_product.review_set.all().order_by('-date_posted') #Most recent reviews first
    review_count = reviews.count()

    # Handle user posting review

    # If the user has just posted a review:
    if request.method == "POST":

        # Get the half-created review object generated by the form
        form = ReviewForm(request.POST)

        # If the form is valid:
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

    # print (rated_users_list.keys())

    # Render page if nothing has gone wrong along the way
    return render(request, 'site360/product_detail.html', {'product_name': correct_product.name, 'product': correct_product, 'reviews': reviews, 'form': form, 'review_count': review_count, 'is_product_favorite': is_product_favorite, 'rated_users_list': rated_users_list, 'current_user_rating': current_user_rating, 'dupes': dupes, 'buy_online': buy_online,})

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
        return redirect('/success')
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
            return redirect('/success?registration')
    else:
        form = UserCreationForm()
    return render(request, 'site360/signup.html', {'form': form})

def profile_info(request, username):
    user = get_object_or_404(User, username=username)
    #profile = Profile.objects.filter(user=user)[0]
    # TO DO: IF USER TRIES TO GET PROFILE, CREATE NEW PROFILE
    favorites = Favorite.objects.filter(user=user).all()

    picture_url = user.profile.picture_url

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

def auth_success(request):
    current_url = request.get_full_path()
    if "?registration" in current_url:
        did_user_just_register = True
    else:
        did_user_just_register = False
    return render(request, 'site360/login-logout-success.html', {'did_user_just_register': did_user_just_register})

def stores(request):
    return render(request, 'site360/stores.html', {})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
