from django.contrib import admin
from .models import Product, Rating, Review

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Rating)
