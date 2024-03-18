from django.contrib.auth.decorators import login_required
from account.models import Profile
from business.models import BusinessProfile,Business_Settings
from bar.models import CartOrders,Order_Summary
from django.db.models import Q
import datetime
from django.utils import timezone
from datetime import timedelta

def active_user(request):
    active_user = []
    active_business = []
    settings = []
    active_order = []
    cart_count = 0
    date_today =  datetime.datetime.now() 
    
    
    if request.user.is_authenticated:
        active_user = Profile.objects.get(user_p = request.user) 
        
        
        if 'activebusiness' in request.session:
            pk = int(request.session['activebusiness'])
            
            last_order = Order_Summary.objects.filter(customer=active_user,order_summary_business__pk = pk).order_by('-date_added').first()
    
            if last_order is None:
                # No orders found for the user
                active_order = []
            else:
                # Get the current time
                current_time = timezone.now()
                
                # Convert last_order.date_added to a datetime object with a time of midnight
                last_order_datetime = timezone.make_aware(datetime.datetime.combine(last_order.date_added, datetime.datetime.min.time()))
            
        
                # Calculate the time difference between the current time and the order's date_added
                time_difference = current_time - last_order_datetime
                
                # Define the threshold for 6 hours
                six_hours = timedelta(hours=6)
                
                # Check if the order is 6 hours old or older
                if time_difference >= six_hours:
                    # Order is 6 hours old or older
                    active_order = last_order.id
                    request.session['active_order'] = active_order
                else:
                    # Order is less than 6 hours old
                    active_order = []
          
            
            
            cart_count = CartOrders.objects.filter(order_by=active_user, source='ONLINE', seller_status=False, buyer_status=False).count()
            active_business = BusinessProfile.objects.get( pk=pk)
            settings = Business_Settings.objects.get(s_business = active_business)
            

        
           
            
    return{
            'active_order':active_order,'date_today':date_today,'active_business':active_business,'active_user':active_user,'settings':settings,'cart_count':cart_count,
            }
    
    #OTHER DEFS WILL RETURN DICTIONARY LIKE CONTEXTS