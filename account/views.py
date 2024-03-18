from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
import os
import secrets
from business.models import My_Business
from .forms import RegisterForm,LoginForm,EditUserForm,EdituserprofileForm
User = get_user_model()
from .models import Profile
def UserProfile(request):
    #launches user profile
    userprofile = Profile.objects.get(user_p = request.user)
    
    return render(request,'account/userprofile/usprofile.html',{'userprofile':userprofile})
    
def RegisterUser(request):
    form = RegisterForm()
    if request.method == 'POST':
        #form registers the user
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            #login user with his profile from the profile model
            user = authenticate(request,phone_number = phone_number,password=password)
            me = Profile(user_p = user)
            me.save()
            login(request, user) 
            def generate_token(length=32):
                return secrets.token_hex(length) 
            token = generate_token()  # Your token generation logic
            request.session['auth_token'] = token 
            
            return redirect('profile')
        else:
            
            return render(request,'account/userprofile/signup.html',{'form':form})
    return render(request,'account/userprofile/signup.html',{'form':form})
    
    
def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        print('POST')
        form = LoginForm(request.POST)
        if form.is_valid():
            #login in and authenticate user with his prfile from te profile model
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request,phone_number = phone_number,password=password)
            login(request, user)
            
            def generate_token(length=32):
                return secrets.token_hex(length) 
            token = generate_token()  # Your token generation logic
            
            request.session['auth_token'] = token 
            try:
                active_user = Profile.objects.get(user_p = request.user) 
                    
                active_business = get_object_or_404(My_Business,business_user = active_user,active_status = True)
                request.session['activebusiness'] =  active_business.business.pk 
                print(request.session['activebusiness'])
            except:
                pass
            return redirect('profile')
        else:
            form.add_error('password','Sorry, that login was invalid. Please try again')
            return render(request,'account/userprofile/login.html',{'form':form})
        
    return render(request,'account/userprofile/login.html',{'form':form})
        
def LogoutView(request):
    #logout the user
    logout(request)
    return redirect('login')
    
def EdituserProfileView(request):
    userprofile = Profile.objects.get(user_p = request.user)
    #Edit user profile from  the profile model
    form = EdituserprofileForm(instance = userprofile)
    if request.method == "POST" :
        form = EdituserprofileForm(request.POST, request.FILES,instance = userprofile)
        
        if form.is_valid():
           
            form.save()
            
        
    return render(request,'account/userprofile/editprofile.html',{'userprofile':userprofile,'form':form})   
    
    
def EdituserView(request):
    form = EditUserForm()
    if request.method == 'POST':
        
        form = EditUserForm(request.POST)
        if form.is_valid():
            
            phone_number = form.cleaned_data.get('phone_number')
            new_phone_number = form.cleaned_data.get('new_phone_number')
            password = form.cleaned_data.get('password')
            password_c = form.cleaned_data.get('password_c')
            print(phone_number)
            print(password_c)
            print(request.user.phone_number)
            print(request.user.password)
            #try:
            user = User.objects.get(phone_number=phone_number, password= password_c)
            user.phone_number = new_phone_number
                
            user.save()
            
            return redirect('profile')
            #except:
                #form.add_error('password_c','Phone number and current password does not match')
            
        else:
            
            return render(request,'account/userprofile/profilesettings.html',{'form':form})
    return render(request,'account/userprofile/profilesettings.html',{'form':form})   
            