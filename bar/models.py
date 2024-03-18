from  django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from business.models import BusinessProfile,Location
from account.models import Profile
User = get_user_model()
mode_choices = [('Not Paid','Not Paid'),('Cash','Cash'),('Mobile Money','Mobile Money')
,('Mobile Money and Cash','Mobile Money and Cash'),('Bank','Bank'),('E-Transfer','E-Transfer')]
type_choices = [('Not Paid','Not Paid'),('Cash','Cash'),('Mobile Money','Mobile Money'),('Merchant','Merchant'),('Credit/Debt Card','Credit/Debt Card')
,('Mobile Money and Cash','Mobile Money and Cash'),('Bank','Bank'),('E-Transfer','E-Transfer')]

mode_choices = [('Pay On Delivery','Pay On Delivery'),('Pay Before Delivery','Pay Before Delivery')]
condition_choices = [('Good','Good'),('Damaged','Damaged')]

order_status_choices = [('Placed','Placed'),('Packed','Packed'),('In Transit','In Transit'),('Delivered','Delivered'),('Pending','Pending')]

purpose_choices = [('Order','Order'),('Shipping','Shipping'),('Additional Fees','Additional Fees'),('Others','Others')]



# Create your models here.
class DrinksCategories(models.Model):
    bar_cat = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'bar_cat') 
    name = models.CharField(max_length=255,null = True, blank = True)
    description = models.TextField(max_length=255,null = True, blank = True)
    category_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'category_by',null = True, blank = True)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.name)        
        
class DrinksSubCategories(models.Model):
    cat = models.ForeignKey(DrinksCategories,on_delete = models.CASCADE, related_name = 'subcategory') 
    name = models.CharField(max_length=255,null = True, blank = True)
    description = models.TextField(max_length=255,null = True, blank = True)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.name)         
        
class DrinksItems(models.Model):
    category = models.ForeignKey(DrinksSubCategories,on_delete = models.CASCADE, related_name = 'category')
    product_name= models.CharField(max_length = 255,null = True,blank = True)
    presentation = models.CharField(max_length=255,null = True, blank = True)
    new_price = models.DecimalField(default=0.0,decimal_places = 1,max_digits=25)
    old_price = models.DecimalField(default=0.0,decimal_places = 1,max_digits=25)
    cover_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(500, 500)],
                                           format='JPEG',
                                           options={'quality': 100})
    availability = models.CharField(max_length = 255,null = True, blank = True)

    brand = models.CharField(max_length=255,null = True, blank = True)
    
    ingridients = models.TextField(max_length=255,null = True, blank = True)
    description = models.TextField(max_length=255,null = True, blank = True)
    minimum_stock_level = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length = 255,null = True, blank = True)
    dimensions = models.CharField(max_length = 255,null = True, blank = True)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.product_name)        
        
 
# Define the Product model
class BarCounterStock(models.Model):
    added_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'added_by',null = True, blank = True)
    stock_owner = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'stock_owner',null = True, blank = True)
    stock_no = models.PositiveIntegerField(default = 0) 
    date_created = models.DateField(auto_now_add = True,null = True, blank = True) 
    def __str__(self):
        return str(self.stock_no)


# Define the Product model
class BarItemStock(models.Model):
    stock = models.ForeignKey(BarCounterStock,on_delete = models.CASCADE, related_name = 'stock',null = True, blank = True)
    stock_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'stock_by',null = True, blank = True)
    bar_item = models.ForeignKey(DrinksItems, on_delete=models.CASCADE)
    good = models.PositiveIntegerField(default=0)
    damaged = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    total_damage_cost = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    purchase_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    quantity_stocked = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.unit_price)
# Define the Product model
class BarInventoryStock(models.Model):
   
    item = models.ForeignKey(DrinksItems,on_delete = models.CASCADE, related_name = 'item',null = True, blank = True)
    quantity_stocked_at_hand = models.PositiveIntegerField(default=0)
    damaged = models.PositiveIntegerField(default=0)
    good = models.PositiveIntegerField(default=0)
    def __str__(self):
        return str(self.item)

class PurchaseOrder(models.Model):
    purchase_order_by = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'purchase_order_by')
    product = models.ForeignKey(DrinksItems, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
   
    order_date = models.DateField()

    def __str__(self):
        return f"Purchase Order for {self.product.name}"

class CloseOpenStock(models.Model):
    open_and_closed_by = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'open_and_closed_by')
    product = models.ForeignKey(DrinksItems, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    
    order_date = models.DateField()

    def __str__(self):
        return f"Purchase Order for {self.product.name}"

       
class CartOrders(models.Model):

    order_product= models.ForeignKey(DrinksItems,on_delete = models.CASCADE, related_name = 'order_product')
    order_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'order_by') 
    worked_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'worked_by',null = True,blank = True)
    product_name = models.CharField(max_length=255,default = 'None')
    product_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(500, 500)],
                                           format='JPEG',
                                           options={'quality': 100})
    quantity = models.CharField(max_length=255)
    price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    total_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    total_order_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    amount_paid = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    balance = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    source = models.CharField(max_length=255,default = 'None')
    buyer_status = models.BooleanField(default = False)
    seller_status = models.BooleanField(default = False)
    recieved_status = models.BooleanField(default = False)
    order_no = models.IntegerField(default = 0)
    order_payement_mode = models.CharField(max_length=255,default = 'Not Paid',choices = type_choices)
    order_transaction_id = models.CharField(max_length=255,default = 'None')
   
    date_added = models.DateField(auto_now_add = True)    
    
    def __str__(self):
    
        return str(self.id)
        
        
class Order_Summary(models.Model):
    order_summary_business = models.ForeignKey(BusinessProfile,on_delete = models.CASCADE, related_name = 'order_summary_business',null = True,blank = True)
    order_s_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'order_s_by',null = True,blank = True) 
    customer = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'customer',null = True,blank = True)
    delivered_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'delivered_by',null = True,blank = True)
    order_no = models.IntegerField(default = 0)
    total = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    shipping_fee = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    date_added = models.DateField(auto_now_add = True)  
    payement_mode = models.CharField(max_length=255,null = True,blank = True)
    paid =  models.CharField(max_length=255,null = True,blank = True)
    balance =  models.CharField(max_length=255,null = True,blank = True)
    code_address = models.ForeignKey(Location,on_delete = models.CASCADE, related_name = 'code_address',null = True,blank = True)
    order_note = models.TextField(null = True,blank = True)
    details = models.TextField(null = True,blank = True)
    source = models.CharField(max_length=255,default = 'None')
    order_status = models.CharField(max_length=255,default = 'Order Placed',choices = order_status_choices)
    payement_status = models.CharField(max_length=255,default = 'Not Paid',choices = mode_choices)
    
    def __str__(self):
    
        return str(self.total)        
       
class Order_Payement(models.Model):
    payed_order = models.ForeignKey(Order_Summary,on_delete = models.CASCADE, related_name = 'payed_order') 
    payement_type = models.CharField(max_length=255,default = 'Not Paid',choices = type_choices)
    payement_mode = models.CharField(max_length=255,default = 'Not Paid',choices = mode_choices)
    
    card_or_merchant_no = models.CharField(max_length=255,null = True,blank = True) 
    recieved_by = models.CharField(max_length=255,null = True,blank = True)
    transaction_id = models.CharField(max_length=255,null = True,blank = True)
    purpose = models.CharField(max_length=255,choices =purpose_choices,default = 'Order')
 
    amount_paid = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    balance = models.DecimalField(default=0,decimal_places = 1,max_digits=25)

    seller_status = models.BooleanField(default = False)

    date_added = models.DateField(auto_now_add = True)    
    
    def __str__(self):
    
        return str(self.payed_order )      
        


class OrderNote(models.Model):
    order_summary_note = models.ForeignKey(Order_Summary,on_delete = models.CASCADE, related_name = 'order_summary_note') 
    note_order_no = models.IntegerField(default = 0)  
    note_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'note_by') 
    order_note = models.TextField(null = True,blank = True)
    delivery_address = models.CharField(max_length=255,null = True,blank = True)
    delivery_contacts = models.CharField(max_length=255,null = True,blank = True)
    shipper_status = models.BooleanField(default = False)
    client_status = models.BooleanField(default = False)
    date_added = models.DateField(auto_now_add = True)    
    
    def __str__(self):
    
        return self.order_note        