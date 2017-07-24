from django import forms
from .models import Product, Profile, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)

class ProfilePictureForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('picture_url',)
		widgets = {'picture_url': forms.TextInput,}
