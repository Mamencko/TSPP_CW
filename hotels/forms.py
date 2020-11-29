from django import forms

from .models import HotelReview


class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ('author', 'email', 'rating', 'text')
