# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('reviews', views.All_Reviews, name='reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/add_reply/', views.add_reply, name='add_reply'),
]