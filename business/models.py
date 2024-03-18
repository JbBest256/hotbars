from  django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from account.models import Profile
User = get_user_model()
mode_choices = [('Not Paid','Not Paid'),('Cash','Cash'),('Mobile Money','Mobile Money')
,('Mobile Money and Cash','Mobile Money and Cash'),('Bank','Bank'),('E-Transfer','E-Transfer')]

# Create your models here.
class BusinessProfile(models.Model):
    business_owner = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'business_owner')
    
    shipping_area = models.CharField(max_length = 255,null = True,blank = True)
    shipping_fee = models.CharField(max_length=255,null = True, blank = True)
    profile_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(500, 500)],
                                           format='JPEG',
                                           options={'quality': 100})
    cover_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           
                                           format='JPEG',
                                           options={'quality': 100})
    business_code = models.CharField(max_length = 255,null = True, blank = True,default = 'ABC')                                       
    business_name = models.CharField(max_length = 255,null = True, blank = True)
    business_address = models.CharField(max_length=255,null = True, blank = True)
    business_location = models.CharField(max_length=255,null = True, blank = True)
    business_slogan = models.CharField(max_length=255,null = True, blank = True)
    business_contacts = models.CharField(max_length= 255,null = True, blank = True)
    about_business = models.TextField(max_length=255,null = True, blank = True)
    business_seo = models.TextField(max_length=255,null = True, blank = True)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.business_name)        
role_choices = [
    ('Admin','Admin'),('Counter','Counter')
    ,('Waiter','Waiter'),('User','User')
    ] 
location_choices = [
    ('Admin','Admin'),('Other','Other')
    
    ]
# Create your models here.
class Business_Settings(models.Model):
    set_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'set_by')
    s_business = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 's_business')
    role = models.CharField(max_length=255,choices = role_choices, default = 'Admin' )
    counter_order_time = models.IntegerField(default = 1 )
    products = models.BooleanField(default = False)
    restaurant = models.BooleanField(default = False)   
    rooms = models.BooleanField(default = False)
    other_services = models.BooleanField(default = False)
    chat = models.BooleanField(default = False)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.s_business)           

# Create your models here.
class My_Business(models.Model):
    business_user = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'business_user')   
    business = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'business')
    role = models.CharField(max_length=255,choices = role_choices, default = 'Admin' )
    
   
    active_status = models.BooleanField(default = False)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.business)

# Create your models here.
class Employee(models.Model):
    employees = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'employees',null = True, blank = True)
    e_business = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'e_business',null = True,blank = True)
    e_added_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'e_added_by',null = True, blank = True)
    title = models.CharField(max_length = 255,null = True,blank = True)
    role_1 = models.BooleanField(default = False)
    role_2 = models.BooleanField(default = False)
    role_3 = models.BooleanField(default = False)
    role_4 = models.BooleanField(default = False)
    role_5 = models.BooleanField(default = False)
    role_6 = models.BooleanField(default = False)
    role_7 = models.BooleanField(default = False)
    role_8 = models.BooleanField(default = False)
    
    active_status = models.BooleanField(default = False)    
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.employees)  

# Create your models here.
class Location(models.Model):
    l_added_by= models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'l_added_by',null = True, blank = True)
    business_l = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'business_l',null = True,blank = True)   
    name = models.CharField(max_length = 255)
    capacity = models.PositiveIntegerField(default=0)
    location_type = models.CharField(max_length=255,choices = location_choices, default = 'Admin' )   
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.name)    

# Create your models here.
class Location_occupied(models.Model):
    location_space = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'location_space')
    occupied = models.BooleanField(default = False)  
    
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.location_space)          


