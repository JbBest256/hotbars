from django import forms
from .models import Review, BusinessOwnerReply

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']

class BusinessOwnerReplyForm(forms.ModelForm):
    class Meta:
        model = BusinessOwnerReply
        fields = ['content']
