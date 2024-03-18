from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm,UserAdminChangeForm
from .models import Profile

from business.models import BusinessProfile,Business_Settings,Employee,My_Business,Location
from bar.models import DrinksItems,DrinksSubCategories,BarCounterStock,CartOrders,Order_Summary,BarInventoryStock
from reviews.models import Review
User = get_user_model()
# Register your models here.


admin.site.unregister(Group)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Location)

admin.site.register(BarInventoryStock)
admin.site.register(My_Business)
admin.site.register(Employee)
admin.site.register(Business_Settings)
admin.site.register(Order_Summary)
admin.site.register(CartOrders)
admin.site.register(BusinessProfile)
admin.site.register(DrinksItems)
admin.site.register(DrinksSubCategories)
admin.site.register(BarCounterStock)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
   
    list_display = ['phone_number','user_name','admin','is_active','staff']
    list_filter = ['admin','is_active','staff']
    fieldsets = ( 
        (None,{'fields':('phone_number','user_name','password')}),
        ('Personal info',{'fields':()}),
        ('Permissions',{'fields':('admin','staff')}),
    
    )
    
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('phone_number','user_name','password','password_2')}
        ),
    )

    search_fields = ['phone_number']
    ordering = ['phone_number']
    filter_horizontal = ()
admin.site.register(User,UserAdmin) 