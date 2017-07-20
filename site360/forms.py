from django import forms
from .models import Product, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)
