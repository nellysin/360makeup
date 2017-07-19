from django.db import models
from django.utils import timezone


class User(models.Model):
    #IN PROGRESS
    username = models.CharField(max_length=20)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    test = ""

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
