from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from .models import BusinessProfile,Employee
from .models import Location
User = get_user_model()



class RegisterBusinessForm(forms.ModelForm):
    cover_image = forms.ImageField(required=False,widget = forms.FileInput(attrs={'multiple':False}))
    profile_image = forms.ImageField(required=False,widget = forms.FileInput(attrs={'multiple':False}))
    class Meta:
        model= BusinessProfile
        fields = ['business_name','business_slogan','business_address','business_location','business_contacts','shipping_area',
        'about_business','business_seo']
        

class AddStaffForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    class Meta:
        model = Employee
        fields = ['phone_number','title']
        
class AddLocationForm(forms.ModelForm):
    
    class Meta:
        model = Location
        fields = ['name','capacity','location_type']        
    