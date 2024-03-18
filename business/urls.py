from django.urls import path
from . import views


urlpatterns = [
   
    path('newbusiness/',views.RegisterBusiness,name ='newbusiness'),
    path('businesssettings/',views.Business_settings,name ='businesssettings'),
    path('bushome/',views.HomeBusiness,name ='bushome'),
    path('mybusiness/',views.MyBusinesses,name ='mybusiness'),
    path('addbusiness/',views.AddBusinessView,name ='addbusiness'),
    path('activatebusiness/',views.ActivateBusinessView,name ='activatebusiness'),
   
    path('staff/',views.BusinessStaff,name ='staff'),
    path('newstaff/',views.AddBusinessStaff,name ='newstaff'),
    
    
    path('activateproducts/',views.ActivateProducts,name ='activateproducts'),
    path('activaterestaurant/',views.ActivateRestaurant,name ='activaterestaurant'),
    path('activaterooms/',views.ActivateRooms,name ='activaterooms'),
    
    
    path('businessloactions/',views.Business_LocationsView,name ='businessloactions'),
    path('addbusinessloactions/',views.CreateBusinessLocations,name ='addbusinessloactions'),
]