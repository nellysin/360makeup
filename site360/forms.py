from django import forms
from .models import Product, Profile, Review

# forms.py controls custom forms.
# There's no need to include forms like login and sign up here
# because we use the automatic forms provided by Django.

class ReviewForm(forms.ModelForm):
    # The form allowing users to write reviews of products
    class Meta:
        model = Review # The information from the form gets plugged into the Review model
        fields = ('body',) # The body of the review comes from the user's input

class ProfilePictureForm(forms.ModelForm):
    # The form where users enter the URL of their profile picture to change it
	class Meta:
		model = Profile
		fields = ('picture_url',)
