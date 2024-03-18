from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class UserManager(BaseUserManager):
    def create_user(self,phone_number,user_name,password=None):
        if not phone_number:
            raise ValueError('User must have a phone number')
        user = self.model(phone_number=phone_number,user_name=user_name)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
        
        
    def create_staffuser(self,phone_number,user_name,password):
        user= self.create_user(phone_number,user_name,password=password)
        user.staff = True
        user.save(using = self._db)
        return user
        
    def create_superuser(self,phone_number,user_name,password):
        user = self.create_user(phone_number,user_name,password=password)
        user.staff = True
        user.admin = True
        user.save(using= self._db)
        return user
        
        
class User(AbstractBaseUser):
    phone_number = PhoneNumberField(unique = True)
    user_name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name']
    objects = UserManager()
    def __str__(self):
        return str(self.phone_number)
    def get_full_name(self):
        return self.user_name
    def get_short_name(self):
        return self.user_name
        
    def has_perm(self,perm,obj=None):
        return True
        
    def has_module_perms(self,app_label):
        return True
        
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
        
        
        
User = get_user_model()
employement_choices = [('At School','At School'),('Employed','Employed'),('Unemployed','Unemployed'),('Self Employed','Self Employed')] 
gender_choices = [('Female','Female'),('Male','Male')] 

# Create your models here.
class Profile(models.Model):
    user_p = models.OneToOneField(User,on_delete = models.CASCADE, related_name = 'user_p')
    cover_image = ProcessedImageField(upload_to='media',blank=True, null=True,format='JPEG',options={'quality': 100})
    
    full_name = models.CharField(max_length=255,null = True,blank = True)
    current_address = models.CharField(max_length=255,null = True,blank = True)
    permanent_address = models.CharField(max_length=255,null = True,blank = True)
    city = models.CharField(max_length=255,null = True,blank = True)
    gender = models.CharField(max_length=255,choices = gender_choices,null = True,blank = True)
    business = models.CharField(max_length=40,null = True, blank = True)
    mobile = models.CharField(max_length=255,null = True,blank = True)
    phone = models.CharField(max_length=255,null = True,blank = True)
    languages = models.CharField(max_length=255,null = True,blank = True)
    employment_status = models.CharField(max_length=255,choices = employement_choices,null = True,blank = True)
    
    email = models.EmailField(null = True,blank = True)

    website = models.CharField(max_length=255,null = True,blank = True)
    facebook = models.CharField(max_length=255,null = True,blank = True)
    instagram = models.CharField(max_length=255,null = True,blank = True)
    twitter = models.CharField(max_length=255,null = True,blank = True)
    github = models.CharField(max_length=255,null = True,blank = True)
    tiktok = models.CharField(max_length=255,null = True,blank = True)
    
    subscribe = models.IntegerField(default = 1)

    about_me = models.TextField(null = True,blank = True)  
    profile_image = ProcessedImageField(upload_to='media',blank=True, null=True,format='JPEG',options={'quality': 100})
    
    def __str__(self):
        return str(self.user_p)+'('+str(self.full_name)+')'
        
