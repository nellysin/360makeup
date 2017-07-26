from django.contrib import admin
from .models import Dupe, Favorite, Product, Profile, Rating, Review

# admin.py controls which models show up in the Admin GUI

# The following models show up:
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Favorite)
admin.site.register(Dupe)
