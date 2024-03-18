from django.urls import path
from . import views


urlpatterns = [
   
    path('signup/',views.RegisterUser,name ='signup'),
    path('',views.UserProfile,name ='profile'),
    path('login/',views.login_user,name ='login'),
    path('logout/',views.LogoutView,name ='logout'),
    path('edituser/',views.EdituserView,name ='edituser'),
    
    path('editprofile/',views.EdituserProfileView,name ='editprofile'),
    
   
   
]