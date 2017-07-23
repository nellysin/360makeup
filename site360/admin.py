from django.contrib import admin
from .models import Favorite, Product, Profile, Rating, Review

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Favorite)
