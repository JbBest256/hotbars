# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm, BusinessOwnerReplyForm
from account.models import Profile
from bar.models import Order_Summary
from django.db.models import Avg


def All_Reviews(request):
    home_b = 3
    # Step 1: Query all reviews and their related replies
    reviews = Review.objects.prefetch_related('reply').all()

    # Step 2: Calculate the average rating from all reviews
    average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
    star_average = int(average_rating)
    # Pass the reviews, their replies, and the average rating to your template
    reply_form = BusinessOwnerReplyForm()
    context = {
        'reviews': reviews,
        'average_rating': average_rating,
        'home_b': home_b,
        'star_average': star_average,
        'reply_form': reply_form
    }
    
    return render(request, 'account/reviews/reviews.html', context)

def add_review(request):
    order = get_object_or_404(Order_Summary, pk=request.session['activemyorder'])
    author = Profile.objects.get(user_p = request.user) 
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.author = author
            review.save()
            return redirect('myordersdetails',)
    else:
        form = ReviewForm()
    return redirect('myordersdetails')

def add_reply(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = BusinessOwnerReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.save()
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = BusinessOwnerReplyForm()
    return render(request, 'add_reply.html', {'form': form})
