from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

class Product(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    company = models.CharField(max_length=100)
    image_url = models.URLField()
    description = models.TextField()
    category = models.CharField(max_length=20, default="Miscellaneous")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    average_rating = models.FloatField()
    number_of_ratings = models.IntegerField()

    def __str__(self):
        return self.name

    def name_to_url(self):
        start_name = self.name
        stripped_name = []
        for char in list(start_name):
            if char == " ":
                stripped_name.append("-")
            elif re.match(r'[A-Z]|[a-z]|[0-9]', char):
                stripped_name.append(char)
        return "".join(stripped_name)

class Review(models.Model):
    date_posted = models.DateTimeField(
            default=timezone.now)
    author = models.ForeignKey('auth.User', null=True)
    body = models.TextField(max_length=1000)
    product = models.ForeignKey(Product, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Rating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    reviewer = models.ForeignKey('auth.User', null=True)

    def __int__(self):
        return self.rating

    def __str__(self):
        return str(self.rating)

    def publish(self):
        self.save()

class Profile(models.Model):
    # In progress
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture_url = models.URLField(null=True)

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', related_name='favorite_user', null=True)
    product = models.ForeignKey(Product, related_name='favorite_product', null=True)
    date_favorited = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.user.username + ": " + str(self.product)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


