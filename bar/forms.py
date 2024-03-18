from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from .models import DrinksCategories,DrinksItems,DrinksSubCategories,BarItemStock
from django.shortcuts import render, redirect,get_object_or_404
from account.models import Profile
User = get_user_model()

class DrinksCategoriesForm(forms.ModelForm):
    class Meta:
        model= DrinksCategories
        fields = ['name','description']

class DrinksSubCategoriesForm(forms.ModelForm):
    class Meta:
        model= DrinksSubCategories
        fields = ['name','description']
                
class AddDrinkItemsForm(forms.ModelForm):
    cover_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'multiple': False}))

    def __init__(self, *args, **kwargs):
        active_business = kwargs.pop('active_business', None)  # Retrieve active_business from kwargs
        super(AddDrinkItemsForm, self).__init__(*args, **kwargs)
        
        if active_business:
            self.fields['category'].queryset = DrinksSubCategories.objects.filter(cat__bar_cat__pk=active_business)

    class Meta:
        model = DrinksItems
        fields = ['product_name', 'presentation', 'new_price', 'old_price', 'brand', 'size', 'dimensions',
                  'minimum_stock_level', 'category', 'availability', 'ingridients', 'description']

        


class AddBarStockItemForm(forms.ModelForm):
    
    item = forms.ModelChoiceField(
        queryset=DrinksItems.objects.all(),
        widget=forms.Select(attrs={'class': 'select2-search'})
    )
    expiry_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input type for modern browsers
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Define accepted input formats
    )
    purchase_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input type for modern browsers
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Define accepted input formats
    )
    class Meta:
        model= BarItemStock
        fields = ['item','good','damaged','unit_price','expiry_date','purchase_date']        
                