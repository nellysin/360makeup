from django.db import models
from django.utils import timezone



class User(models.Model):
    #IN PROGRESS
    username = models.CharField(max_length=20)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username


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
        return self.name.replace(" ", "-")


class Review(models.Model):
    date_posted = models.DateTimeField(
            default=timezone.now)
    body = models.CharField(max_length=1000)
    product = models.ForeignKey(Product)
