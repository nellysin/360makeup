from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

class Product(models.Model):
    name = models.CharField(max_length=100)
    # When the product was added to the database
    created_date = models.DateTimeField(default=timezone.now)

    company = models.CharField(max_length=100)
    image_url = models.URLField()
    description = models.TextField()
    category = models.CharField(max_length=20, default="Miscellaneous")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Sites where users can buy the product online
    buy_online = models.TextField(default="", blank=True, null=True)

    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    number_of_ratings = models.IntegerField()

    def __str__(self):
        # The admin site will display the products by their names
        return self.name

    def name_to_url(self):
        # If the product name has special characters in it,
        # those get stripped out in the URL for its product page
        start_name = self.name
        stripped_name = []
        for char in list(start_name):

            # Spaces are replaced by dashes
            if char == " ":
                stripped_name.append("-")

            # Numbers and letters remain as they are
            elif re.match(r'[A-Z]|[a-z]|[0-9]', char):
                stripped_name.append(char)

            # If a character is neither dash nor number/letter, it's removed

        return "".join(stripped_name)

    def buy_online_to_list(self):
        # Credit to StackOverflow

        # The buy_online table is in this format:
        # URL
        # name of site

        # buy_online_to_list splits the table into lists of lists
        # where each sub-list is in the format [URL, name of site]

        #Splits buy_online lines
        if "\n" in self.buy_online:
            buy_online = self.buy_online.split("\n")

            # Returns buy_online split into sub-lists of two elements each
            return [buy_online[i:i + 2] for i in range(0, len(buy_online), 2)]

        #If there are no new lines, there probably aren't any places to buy it online
        return False

class Review(models.Model):
    # The date the review was written
    date_posted = models.DateTimeField(
            default=timezone.now)
    # The product the review is for
    product = models.ForeignKey(Product, null=True)
    # The user who wrote the review
    author = models.ForeignKey('auth.User', null=True)
    # The text of the review
    body = models.TextField(max_length=1000)

    def __str__(self):
        # In the admin site, displays the author's username plus a bit of the review
        if self.author:
            return self.author.username + ": " + self.body[:30]
        else:
            return "None: " + self.body[:30]

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Rating(models.Model):
    # Ratings out of five stars

    # The numerical value of the rating
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    # The person who rated the product
    reviewer = models.ForeignKey('auth.User', null=True)
    # The product rated
    product = models.ForeignKey('Product', null=True)

    def __int__(self):
        return int(self.rating)

    def __str__(self):
        # On admin, displays the reviewer, the rating, and the product
        if self.reviewer and self.rating and self.product:
            return self.reviewer.username + ": " + self.product.name + ", " + str(self.rating)
        else:
            return "None"

    def publish(self):
        self.save()

class Profile(models.Model):
    # Profile extends Django's existing user class
    # So each created user has a corresponding profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # The URL of the user's profile picture
    picture_url = models.URLField(null=True)

    def __str__(self):
        return self.user.username

# Credit to Simpleisbetterthancomplex
# With these two functions, every time a user gets created, a corresponding
# profile is generated, and every time the user object is modified, their profile
# object is modified as well.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', related_name='favorite_user', null=True)
    product = models.ForeignKey('Product', related_name='favorite_product', null=True)
    date_favorited = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.user.username + ": " + str(self.product)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Dupe(models.Model):
    product = models.ForeignKey('Product', null=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    url = models.URLField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name + " (dupe of " + self.product.name + ")"
