from django.shortcuts import render, redirect,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
import os
from .forms import RegisterBusinessForm,AddStaffForm,AddLocationForm
User = get_user_model()
from .models import BusinessProfile,Employee,Business_Settings,My_Business,Location
from account.models import Profile
# Create your views here.


def RegisterBusiness(request):
    #register business form
    form = RegisterBusinessForm()
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        
        form = RegisterBusinessForm(request.POST,request.FILES)
        
        #check if there is an active business and deactivate it
        try:
            active_bus = My_Business.objects.get(business = current_user, active_status = True)
            if active_bus:
                active_bus.active_status = False
                active_bus.save()
        except:
            pass
            
        if form.is_valid():
           
            bus = form.save(commit=False)
            if request.FILES.get('cover_image'):
                cover_image = request.FILES.get('cover_image')
                #get the cover image because it wont be saved directly
                bus.cover_image = cover_image
               
            if request.FILES.get('profile_image'):
                
                profile_image = request.FILES.get('profile_image')
                #get the profile_image because it wont be saved imediately
                bus.profile_image = profile_image     
            bus.business_owner = current_user
            #save business
            bus.save()
            Employee.objects.create(employees = current_user,role_1 = True, e_business = bus,active_status=True)
            Business_Settings.objects.create(set_by = current_user,role = 'Admin', s_business = bus)
            My_Business.objects.create(business_user = current_user,role = 'Admin', business = bus,active_status = True)
            request.session['activebusiness'] = bus.pk
            print(request.session['activebusiness'])
            print(bus.pk)
            return redirect('bushome')
        else:
            
            return render(request,'account/business/newbusiness.html',{'form':form})
    return render(request,'account/business/newbusiness.html',{'form':form})
    
    
def HomeBusiness(request):
    
    home_b = 122
    return render(request,'account/business/home.html',{'home_b':home_b})

def Business_settings(request):
    #My business view, fetches business of the current loged in user and sets the active business session
    current_user = get_object_or_404(Profile,user_p = request.user)
    #business must be current active business
    settings= get_object_or_404(Business_Settings,s_business__pk =  request.session['activebusiness'])
    locations = Location.objects.filter(business_l__pk = request.session['activebusiness'])
    return render(request,'account/business/businesssettings.html',{'settings':settings,'locations':locations})
    
#view to business locations    
def CreateBusinessLocations(request):
    
    form = AddLocationForm()
    current_user = get_object_or_404(Profile,user_p = request.user)
    current_business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    if request.method == 'POST':
        
        form = AddLocationForm(request.POST,request.FILES)
        if form.is_valid():
            location = form.save(commit=False)
            location.business_l = current_business
            location.l_added_by = current_user
            location.save()
           
            return redirect('businessloactions')
        else:
            
            return render(request,'account/business/newlocation.html',{'form':form})
    return render(request,'account/business/newlocation.html',{'form':form})
    
def Business_LocationsView(request):
    #My business view, fetches business of the current loged in user and sets the active business session
    current_user = get_object_or_404(Profile,user_p = request.user)
    current_business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    locations = Location.objects.filter(business_l = current_business)
    
    return render(request,'account/business/businesslocations.html',{'locations':locations})


#business activation view
def ActivateRestaurant(request):
   #since a user can create different businesses, each business can be activated
    if request.method == 'POST':
       
        messagess = json.loads(request.body)
        #get loged in user
        current_user = get_object_or_404(Profile,user_p = request.user)
        settings = get_object_or_404(Business_Settings,pk = messagess)
        if settings.restaurant == False:
            settings.restaurant = True
            settings.save()
        else:
            settings.restaurant = False
            settings.save()
   
    message_list = [{
      
        'message':'success',
      
    }]
   #active business session is not set
    return JsonResponse(message_list,safe=False)                 


#business activation view
def ActivateProducts(request):
   #since a user can create different businesses, each business can be activated
    if request.method == 'POST':
       
        messagess = json.loads(request.body)
        #get loged in user
        current_user = get_object_or_404(Profile,user_p = request.user)
        settings = get_object_or_404(Business_Settings,pk = messagess)
        if settings.products == False:
            settings.products = True
            settings.save()
        else:
            settings.products = False
            settings.save()
   
    message_list = [{
      
        'message':'success',
      
    }]
   #active business session is not set
    return JsonResponse(message_list,safe=False)                 

#business activation view
def ActivateRooms(request):
   #since a user can create different businesses, each business can be activated
    if request.method == 'POST':
       
        messagess = json.loads(request.body)
        #get loged in user
        current_user = get_object_or_404(Profile,user_p = request.user)
        settings = get_object_or_404(Business_Settings,pk = messagess)
        if settings.rooms == False:
            settings.rooms = True
            settings.save()
        else:
            settings.rooms = False
            settings.save()
   
    message_list = [{
      
        'message':'success',
      
    }]
   #active business session is not set
    return JsonResponse(message_list,safe=False)                 
#business activation view
def AddBusinessView(request):
   #since a user can create different businesses, each business can be activated
    if request.method == 'POST':
        message_list = [{
      
        'message':'success',
      
    }]
        messagess = json.loads(request.body)
        #get loged in user
        current_user = get_object_or_404(Profile,user_p = request.user)
        try:
            business = get_object_or_404(BusinessProfile,business_code = messagess)
            try:
                active_bus = My_Business.objects.get(business_user = current_user,business= business)
                if active_bus.active_status ==False:
                    active_bus.active_status = True
                    active_bus.save()
            except:
                try:
                    active_bus = My_Business.objects.get(business_user = current_user, active_status = True)
                    active_bus.active_status =False
                    active_bus.save()
                except:
                    pass
                My_Business.objects.create(business_user = current_user,role = 'User', business = business,active_status = True)
                
        except:
            message_list = [{
      
        'message':'nobusiness',
      
    }]
        try:
            active_bus = My_Business.objects.get(business_user = current_user, active_status = True)
            request.session['activebusiness'] = active_bus.business.pk
        except:
            pass
   
    
   #active business session is not set
    return JsonResponse(message_list,safe=False)                 


    
    
def MyBusinesses(request):
    #Get all businesses the user has created 
    current_user = get_object_or_404(Profile,user_p = request.user)
    businesses = My_Business.objects.filter(business_user = current_user,)
    #get that only active business the user has
    assoc = []
    try:
        assoc = get_object_or_404(My_Business,business_user = current_user, active_status = True)
    except:
        pass
    return render(request,'account/business/mybusinesses.html',{'assoc':assoc,'businesses':businesses})

#business activation view
def ActivateBusinessView(request):
   #since a user can create different businesses, each business can be activated
    if request.method == 'POST':
    
        messagess = json.loads(request.body)
        #get loged in user
        current_user = get_object_or_404(Profile,user_p = request.user)
        active_bus=[]
        #this view automatically activates and deactivates the business
        activated_bus = My_Business.objects.get(pk = messagess )
        if activated_bus.active_status == True:
            activated_bus.active_status = False
            del request.session['activebusiness']
            activated_bus.save()
        else:
            #first deactivate any active business the activate the sent business via ajax
            try:
                active_bus = My_Business.objects.get(business_user = current_user, active_status = True)
                active_bus.active_status =False
                active_bus.save()
                
            except:
                pass
            activated_bus.active_status = True
            activated_bus.save()
        try:
            active_bus = My_Business.objects.get(business_user = current_user, active_status = True)
            request.session['activebusiness'] = active_bus.business.pk
        except:
            pass
   
    message_list = [{
      
        'message':'success',
      
    }]
   #active business session is not set
    return JsonResponse(message_list,safe=False)                 







def BusinessStaff(request):
    #
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    #request.session['activebusiness'] = business.pk
    staffs = Employee.objects.filter(e_business = business)
    return render(request,'account/business/staff.html',{'staffs':staffs})    
    
    #business activation view
def AddBusinessStaff(request):
    #register business form
    form = AddStaffForm()
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    if request.method == 'POST':
        
        form = AddStaffForm(request.POST,request.FILES)
        
            
        if form.is_valid():
           
           
            phone_number = form.cleaned_data['phone_number']
            
            worker = Profile.objects.get(user_p__phone_number = phone_number)
            #check if user is already a worker of given business
            try:
                is_employee = Employee.objects.get(employees = worker, e_business = business)
            except:
                
                title = form.cleaned_data['title']
                try:
                    role_1 = int(request.POST.get('role_1'))     
                
                    role_1 = True
                except:
                    role_1 = False
                try:    
                    role_2 = int(request.POST.get('role_2'))
                
                    role_2 = True
                except:
                    role_2 = False
                try:    
                    role_3 = int(request.POST.get('role_3'))
                
                    role_3 = True
                except:
                    role_3 = False
                try:    
                    role_4 = int(request.POST.get('role_4'))
                
                    role_4 = True
                except:
                    role_4 = False
                try:    
                    role_5 = int(request.POST.get('role_5'))
                
                    role_5 = True
                except:
                    role_5 = False
                try:    
                    role_6 = int(request.POST.get('role_6'))
                
                    role_6 = True
                except:
                    role_6 = False
                try:    
                    role_7 = int(request.POST.get('role_7'))
                
                    role_7 = True
                except:
                    role_7 = False
                try:    
                    role_8 = int(request.POST.get('role_8'))
                
                    role_8 = True
                except:
                    role_8 = False
               
                Employee.objects.create(role_1 = role_1,role_2 = role_2,
                role_3 = role_3,role_4 = role_4,role_5 = role_5,role_6 = role_6,role_7 = role_7,role_8 = role_8,
                title = title,employees = worker, e_business = business,)                                                                                     
            return redirect('staff')
        else:
            
            return render(request,'account/business/newstaff.html',{'form':form})
    return render(request,'account/business/newstaff.html',{'form':form})   