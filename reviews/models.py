# models.py
from django.db import models
from bar.models import Order_Summary
from account.models import Profile
class Review(models.Model):
    order = models.ForeignKey(Order_Summary, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField()  # Rating can be from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
    
        return str(self.content) 

class BusinessOwnerReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
