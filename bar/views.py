from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json,os
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from account.models import Profile
from business.models import BusinessProfile,Employee,Location
from .forms import DrinksCategoriesForm,AddDrinkItemsForm,DrinksSubCategoriesForm,AddBarStockItemForm
from .models import DrinksCategories,DrinksItems,DrinksSubCategories,BarCounterStock,BarItemStock,BarInventoryStock,CartOrders,Order_Summary
from reviews.forms import ReviewForm
User = get_user_model()
def HomeView(request):
    
    return render(request,'account/bar/profile.html')
#Bar pont of sale view    
def SetCategoryView(request):
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        if messagess == 0:
            if 'activecategory' in request.session:
                del request.session['activecategory']
        else:        
            request.session['activecategory']=messagess
        
            
        message_list = [{
            
            'message': 'success',
        }]

        return JsonResponse(message_list, safe=False)     
#Bar pont of sale view    
def PointOfSale(request):
    business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    current_user = get_object_or_404(Profile,user_p = request.user)
    carts = CartOrders.objects.filter(order_by=current_user, source='POS', seller_status=False, buyer_status=False)    
    ordered_carts = Order_Summary.objects.filter(order_s_by=current_user,order_summary_business=business,  source='POS')
    categories = DrinksSubCategories.objects.filter(cat__bar_cat = business)
    waiters = Employee.objects.filter(e_business=business,role_5 =True)
    if 'activecategory' in request.session:
        products = BarInventoryStock.objects.filter(quantity_stocked_at_hand__gt = 0,item__category__cat__bar_cat = business, item__category__pk = request.session['activecategory'])
        active = request.session['activecategory']
    else:
        products = BarInventoryStock.objects.filter(item__category__cat__bar_cat = business,quantity_stocked_at_hand__gt = 0)
        active = 0
    return render(request,'account/bar/pos.html',{'active':active,'categories':categories,'waiters':waiters,'products':products,'carts':carts,'ordered_carts':ordered_carts})

#Bar pont of sale view    
def PointOfSaleOnlineOrders(request):
    business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    current_user = get_object_or_404(Profile,user_p = request.user)
      
    ordered_carts = Order_Summary.objects.filter(order_summary_business=business,delivered_by = None,  source='ONLINE')
    
    
    return render(request,'account/bar/posonlineorders.html',{'ordered_carts':ordered_carts})
    
@login_required(login_url = 'logout')    
def PointOfSaleOnlineOrdersDetailsAjax(request):
    
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        request.session['activeposonlineorder'] = messagess
        
        message_list = [{
            
            'message': 'success',
        }]

        return JsonResponse(message_list, safe=False)
#Bar pont of sale view    
def OnlineOrderDetails(request):
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    ordered_carts = CartOrders.objects.filter(order_product__category__cat__bar_cat =business, order_no = request.session['activeposonlineorder'])
    ordersummary = Order_Summary.objects.get(source='ONLINE',order_no = request.session['activeposonlineorder'], order_summary_business = business)
    waiters = Employee.objects.filter(e_business=business,role_5 =True)
    return render(request,'account/bar/onlineorderdetails.html',{'waiters':waiters,'ordered_carts':ordered_carts,'ordersummary':ordersummary})
@login_required(login_url = 'logout')    
def PlaceOnlineOrderToWaiter(request):
    
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        waiter = Profile.objects.get(pk = messagess)
        business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
        order =  Order_Summary.objects.get(source='ONLINE', order_no = request.session['activeposonlineorder'], order_summary_business = business)
        order.delivered_by = waiter
        order.order_status = 'Placed'
        order.save()
        
        message_list = [{
            
            'message': 'success',
        }]

        return JsonResponse(message_list, safe=False)
#Bar pont of sale view    
def PointOfSaleOrders(request):
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    ordered_carts = Order_Summary.objects.filter(order_summary_business=business,  source='POS')

    
    return render(request,'account/bar/posorders.html',{'ordered_carts':ordered_carts})
    
#Bar pont of sale view    
def MyOrdersView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    ordered_carts = Order_Summary.objects.filter(order_summary_business=business,customer =current_user )

    
    return render(request,'account/bar/myorders.html',{'ordered_carts':ordered_carts})
        
#Bar pont of sale view    
def MyassignedPointOfSaleOrders(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    ordered_carts = Order_Summary.objects.filter(order_summary_business=business,  delivered_by=current_user)

    
    return render(request,'account/bar/myassignedposorders.html',{'ordered_carts':ordered_carts})
    
@login_required(login_url = 'logout')    
def ChangeOrderStatusAjaxView(request):
    
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        request.session['activeordertobechanged'] = messagess
        
        message_list = [{
            
            'message': 'success',
        }]

        return JsonResponse(message_list, safe=False)
        
      
#Bar pont of sale view    
def OrderStatusView(request):
    ordersummary = Order_Summary.objects.get(pk=request.session['activeordertobechanged'])
    orders = CartOrders.objects.filter(order_no = ordersummary.order_no)

    
    return render(request,'account/bar/changeorderstatus.html',{'orders':orders,'ordersummary':ordersummary})  
@login_required(login_url = 'logout')    
def MyOrdersDetailsAjaxView(request):
    
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        request.session['activemyorder']= messagess
        
        message_list = [{
            
            'message': 'success',
        }]

        return JsonResponse(message_list, safe=False)
                  
#Bar pont of sale view    
def MyOrdersDetailsView(request):
    ordersummary = Order_Summary.objects.get(pk=request.session['activemyorder'])
    orders = CartOrders.objects.filter(order_no = ordersummary.order_no)
    review_form = ReviewForm()
    star_range = range(1, 6) 
    return render(request,'account/bar/recentorderdetails.html',{'star_range':star_range,'review_form':review_form,'orders':orders,'ordersummary':ordersummary})            

#Bar pont of sale view    
def ChangeOrderStatusView(request):
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        order = Order_Summary.objects.get(pk = request.session['activeordertobechanged'])
        if messagess == 1:
            order.order_status = 'Packed'
            order.save()
        elif messagess == 2: 
            order.order_status = 'In Transit'
            order.save()
        elif messagess == 3:
            order.order_status = 'Delivered'
            order.save()
        elif messagess == 0:
            order.order_status = 'Placed'
            order.save()
            
        message_list = [{
            
            'message': 'success',
        }]

        return JsonResponse(message_list, safe=False)    
#Bar counter view    
def CounterView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    products = BarInventoryStock.objects.filter(item__category__cat__bar_cat = business, quantity_stocked_at_hand__gt = 0)
    incart = CartOrders.objects.filter(order_by=current_user, source='ONLINE', seller_status='False', buyer_status='False')
    home_b = 122
    return render(request,'account/bar/counter.html',{'products':products,'incart':incart,'home_b':home_b})
    
#Counter categories view to view bar item categories 
def CounterCatsView(request):
    #activate business
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    categories= DrinksCategories.objects.annotate(subcatery_count = Count('subcategory')).prefetch_related('subcategory').filter(bar_cat = business)
    
    return render(request,'account/bar/countercategories.html',{'categories':categories})
    
#view to display counter items to the admin
def CounterItemsView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    items = DrinksItems.objects.filter(category__cat__bar_cat = business)
    
    return render(request,'account/bar/counteritems.html',{'items':items}) 
    
#view to display stocks to the admin    
def BarStockView(request):
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    items = BarItemStock.objects.filter(stock__pk =request.session['stockon'], stock__stock_owner = business)
    return render(request,'account/bar/stock.html',{'items':items})           
    
def BarStocksView(request):
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
     

    # Use annotate to add a calculated field to all Stock objects that represents the sum of prices in related StockItem instances
    items = BarCounterStock.objects.filter(stock_owner = business).annotate(total_purchase=Sum('stock__total_price'),total_damage=Sum('stock__total_damage_cost'))


    return render(request,'account/bar/stocks.html',{'items':items}) 

#view to display current stock to the admin    
def BarCurrentStock(request):
  
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    items = BarInventoryStock.objects.filter(item__category__cat__bar_cat = business)
    return render(request,'account/bar/currentstock.html',{'items':items})           

#view to add categories to bar items    
def CreateBarCategories(request):
    
    form = DrinksCategoriesForm()
    current_user = get_object_or_404(Profile,user_p = request.user)
    current_business = get_object_or_404(BusinessProfile,pk = request.session['activebusiness'])
    if request.method == 'POST':
        
        form = DrinksCategoriesForm(request.POST,request.FILES)
        if form.is_valid():
            categories = form.save(commit=False)
            categories.bar_cat = current_business
            categories.save()
           
            return redirect('countercats')
        else:
            
            return render(request,'account/bar/newcategories.html',{'form':form})
    return render(request,'account/bar/newcategories.html',{'form':form})
    
#ajax view to add subcategores    
def AjaxAddBarSubCategory(request):
   
    if request.method == 'POST':
       
        messagess = json.loads(request.body)
        request.session['addtobarsubcategory'] = messagess
        
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)  
    
#non ajax view to add subcategores
def AddBarSubCategory(request):
    form = DrinksSubCategoriesForm()
    
    if request.method == 'POST':
        
        form = DrinksSubCategoriesForm(request.POST)
        if form.is_valid():
            subcats = form.save(commit=False)
            cat = DrinksCategories.objects.get(pk = request.session['addtobarsubcategory'])
            if 'addtobarsubcategory' in request.session:
                del request.session['addtobarsubcategory']    
            subcats.cat = cat
            subcats.save()
            return redirect('countercats')
        else:
            
            return render(request,'account/bar/newitem.html',{'form':form})
    return render(request,'account/bar/newitem.html',{'form':form})


#view to create bar items
def CreateBarItem(request):
    active_business = request.session.get('activebusiness')
    form = AddDrinkItemsForm(active_business=active_business)  # Pass active_business as a keyword argument
    
    if request.method == 'POST':
        form = AddDrinkItemsForm(request.POST, request.FILES, active_business=active_business)
        if form.is_valid():
            item = form.save(commit=False)
            cover_image = request.FILES.get('cover_image')
            if cover_image:
                item.cover_image = cover_image
            
            item.save()
            BarInventoryStock.objects.create(item=item)
            
            return redirect('counteritems')
            
    return render(request, 'account/bar/newitem.html', {'form': form})

#view to add new stock to the
def CreateBarStock(request):
    #get business owner and business profile
    current_user = get_object_or_404(Profile, user_p=request.user)
    business = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
    #use transaction key word to avoid double stocks
    try:
        with transaction.atomic():
            last_stock = BarCounterStock.objects.filter(stock_owner=business).order_by('-id')[0]
            new_stock_no = last_stock.stock_no + 1
    except IndexError:
        new_stock_no = 1
    #new stock is added with new stock number
    new_stock = BarCounterStock.objects.create(stock_no=new_stock_no,added_by=current_user,stock_owner=business)
    #new stock number is stored as a session
    request.session['stockon'] = new_stock.pk
    return redirect('barstock')

#ajax view to store any stock numberadmin wants to view
def AjaxBarStock(request):
   
    if request.method == 'POST':
       
        messagess = json.loads(request.body)
        if 'stockon' in request.session:
            del request.session['stockon']
        request.session['stockon'] = messagess
        
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)                   

#add new stock items to stocks       
def CreateBarStockItem(request):
    form = AddBarStockItemForm()
    current_user = get_object_or_404(Profile, user_p=request.user)
    if request.method == 'POST':
        
        form = AddBarStockItemForm(request.POST)
        if form.is_valid():
            #get current stock
            current_stock = BarCounterStock.objects.get(pk = request.session['stockon'] )
            stock = form.save(commit=False)
            #add required fields for the stock
            bar_item = form.cleaned_data['item']
            price = form.cleaned_data['unit_price']
            
            good = form.cleaned_data['good']
            damaged = form.cleaned_data['damaged']
            quantity = good+damaged
            stock.quantity_stocked = quantity
            stock.total_price = price*quantity
            stock.bar_item = bar_item
            stock.stock = current_stock
            stock.stock_by = current_user
            stock.save()
            #save item and its quantity in the inventory stock to calculate its current quantity, keeping its original stock values
            #in the bar stock table
            inventorystock = BarInventoryStock.objects.get(item = bar_item)
           
            inventorystock.quantity_stocked_at_hand += quantity
            
            inventorystock.good += good
            
            inventorystock.damaged += damaged
            inventorystock.save() 
            
            return redirect('barstock')
        else:
            
            return render(request,'account/bar/newitem.html',{'form':form})
    return render(request,'account/bar/newitem.html',{'form':form})
    
  
########### CART POS MARKET##############
#ajax view to add items to pos cart
@login_required(login_url = 'logout')    
def AddToPosCartView(request):
    #recieve product ID using Ajax 
    if request.method == 'POST':
        current_user = get_object_or_404(Profile, user_p=request.user)
        messagess = json.loads(request.body)

    try:
        item = CartOrders.objects.get(order_by=current_user, order_product__pk=messagess, buyer_status=False)
        message_list = [{
            'message': 'none',
        }]
        return JsonResponse(message_list, safe=False)
    except CartOrders.DoesNotExist:
        # If product is not in the cart, add it
        product = DrinksItems.objects.get(pk=messagess)
        order_product = product
        order_by = current_user
        quantity = 1
        price = product.new_price
        total_price = product.new_price
        product_image = product.cover_image.url
        product_name =product.product_name
        CartOrders.objects.create(product_name = product_name,product_image = product_image,source='POS', order_product=order_product, order_by=order_by, quantity=quantity, price=price, total_price=total_price)
        products = CartOrders.objects.filter(order_by=order_by, source='POS', seller_status=False, buyer_status=False)

        # Convert the QuerySet to a list of dictionaries
        product_list = serializers.serialize('python', products)
        products = [{'pk': item['pk'], 'fields': item['fields']} for item in product_list]
        
        message_list = [{
            
            'products': products,
        }]

        return JsonResponse({
            'products': products,
        }, safe=False)

#REMOVE A PRODUCT FROM A POS CART
@login_required(login_url = 'logout')    
def RemoveFromPosCartView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        item = CartOrders.objects.get(pk=messagess)
        item.delete()
        
        
        products = CartOrders.objects.filter(order_by=current_user, source='POS', seller_status=False, buyer_status=False)

        # Convert the QuerySet to a list of dictionaries
        product_list = serializers.serialize('python', products)
        products = [{'pk': item['pk'], 'fields': item['fields']} for item in product_list]
        
        message_list = [{
            
            'products': products,
        }]

        return JsonResponse({
            'products': products,
        }, safe=False)
    
#CHANGE QUANTITY OF A POS CART
@login_required(login_url = 'logout')    
def ChangeQtyFromPosCartView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        pk = messagess['id']
        qty = messagess['qty']
        item = CartOrders.objects.get(pk=pk)
        item.quantity = qty
        price = int(qty)*int(item.total_price)
        item.total_price = price
        item.save()
        
        products = CartOrders.objects.filter(order_by=current_user, source='POS', seller_status=False, buyer_status=False)

        # Convert the QuerySet to a list of dictionaries
        product_list = serializers.serialize('python', products)
        products = [{'pk': item['pk'], 'fields': item['fields']} for item in product_list]
        
        message_list = [{
            
            'products': products,
        }]

        return JsonResponse({
            'products': products,
        }, safe=False)
        
        
#POS CHECKOUT ORDER VIEW
@login_required(login_url = 'logout')    
def PosCheckOutView(request):
   
    if request.method == 'POST':
        
        #GET ALL SENT DATA, ADDRESS AND PAYEMENT MODE
        messagess = json.loads(request.body)
        payement_mode = messagess['payment_mode']
        address_code = messagess['address_code']
        paid = messagess['paid']
        balance = messagess['balance']
        total_price = messagess['total_price']
        order_note = messagess['order_note']
        waiter = int(messagess['waiter'])
        
        waiter = Profile.objects.get(pk = waiter)
        current_user = get_object_or_404(Profile,user_p = request.user)
        businesses = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
        
        last_order = CartOrders.objects.filter(source='POS',order_by =current_user,buyer_status = True,seller_status = True).order_by('-id')
        #get last order to assign an order number    
        if last_order:
            last_order = last_order[0]
            order_no = int(last_order.order_no)+1
            orders = CartOrders.objects.filter(source='POS',order_by =current_user,buyer_status = False,seller_status = False)
            details = ', '.join(order.product_name+'('+order.quantity+')' for order in orders)
            
            Order_Summary.objects.create(
            order_s_by = current_user,order_no=order_no,total=total_price,payement_mode = payement_mode,order_summary_business = businesses,
            balance = balance,order_note=order_note,code_address=address_code,paid = paid,source='POS',delivered_by=waiter,details=details
            )  
            
            
            for order in orders:
                current_stock = BarInventoryStock.objects.get(item__pk = order.order_product.pk)
                
                remaining_stock = int(current_stock.good)-int(order.quantity)
                print(current_stock.quantity_stocked_at_hand)
                remaining_stock_at_hand = current_stock.quantity_stocked_at_hand - int(order.quantity)
                current_stock.good = remaining_stock
                current_stock.quantity_stocked_at_hand = remaining_stock_at_hand
                current_stock.save()
                
            orders.update(seller_status = True,buyer_status = True,order_no =order_no)
                
            #save order summary 
            message_list = [{
      
                'message':'success',
      
                }]   
                
            
        else:
            orders = CartOrders.objects.filter(source='POS',order_by =current_user,buyer_status = False,seller_status = False)
            details = ', '.join(order.product_name+'('+order.quantity+')' for order in orders)
            
            Order_Summary.objects.create(
            order_s_by = current_user,order_no=1,total=total_price,payement_mode = payement_mode,
            balance = balance,order_note=order_note,code_address=address_code,paid = paid,source='POS',
            delivered_by=waiter,details=details,order_summary_business = businesses
            )  
            
            
            for order in orders:
                current_stock = BarInventoryStock.objects.get(item__pk = order.order_product.pk)
                
                remaining_stock = int(current_stock.good)-int(order.quantity)
                print(current_stock.quantity_stocked_at_hand)
                remaining_stock_at_hand = current_stock.quantity_stocked_at_hand - int(order.quantity)
                current_stock.good = remaining_stock
                current_stock.quantity_stocked_at_hand = remaining_stock_at_hand
                current_stock.save()
                
            orders.update(seller_status = True,buyer_status = True,order_no =1)
            message_list = [{
      
                'message':'success',
      
                }]    
            #save order summary 
            
        message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False) 

        
        
########### CART MARKET##############

#Counter Cart VIEW    
def CounterCartView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    locations = Location.objects.filter(location_type ='Other', business_l__pk = request.session['activebusiness'])
    carts = CartOrders.objects.filter(order_by=current_user, source='ONLINE', seller_status=False, buyer_status=False)
    total_price = sum(cart.total_price for cart in carts if cart.total_price is not None)
    
    return render(request,'account/bar/cart.html',{'locations':locations,'carts':carts,'total_price':total_price})

def TrackCounterOrderView(request):
    #recieve product ID using Ajax 
    if request.method == 'POST':
        current_user = get_object_or_404(Profile,user_p = request.user)
        messagess = json.loads(request.body)
        
        order = Order_Summary.objects.get(order_no = messagess)
        order.customer = current_user
        order.save()
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False) 

#ADD ITEM TO CART
@login_required(login_url = 'logout')    
def AddtoCartView(request):
    #recieve product ID using Ajax 
    if request.method == 'POST':
        current_user = get_object_or_404(Profile,user_p = request.user)
        messagess = json.loads(request.body)
        #check if a product is in the cart not bought yet and dont add the product again, buyer status false
        try:
            item = Orders.objects.get(order_by =current_user,order_product__pk =messagess,buyer_status = False)
            message_list = [{
      
        'message':'none',
      
    }]
   
            return JsonResponse(message_list,safe=False)  
        except:
            #if product not there yet, we add the product to the orders
            product = DrinksItems.objects.get(pk = messagess)
            order_product = product
            order_by = current_user
            quantity = 1
            price = product.new_price
            total_price = product.new_price
            product_image = product.cover_image.url
            product_name =product.product_name
            CartOrders.objects.create(product_name = product_name,product_image = product_image,source='ONLINE', order_product=order_product, order_by=order_by, quantity=quantity, price=price, total_price=total_price)
            
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)  
    
#Remove item from COUNTER cart                                          
@login_required(login_url = 'logout')    
def RemoveFromCounterCartView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        item = CartOrders.objects.get(pk=messagess)
        item.delete()
        
        
        products = CartOrders.objects.filter(order_by=current_user, source='ONLINE', seller_status=False, buyer_status=False)

        # Convert the QuerySet to a list of dictionaries
        product_list = serializers.serialize('python', products)
        products = [{'pk': item['pk'], 'fields': item['fields']} for item in product_list]
        
        message_list = [{
            
            'products': products,
        }]

        return JsonResponse({
            'products': products,
        }, safe=False)
    

#CHANGE QUANTITY OF A POS CART
@login_required(login_url = 'logout')    
def ChangeQtyFromCounterCartView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        pk = messagess['id']
        qty = messagess['qty']
        item = CartOrders.objects.get(pk=pk)
        item.quantity = qty
        price = int(qty)*int(item.total_price)
        item.total_price = price
        item.save()
        
        products = CartOrders.objects.filter(order_by=current_user, source='ONLINE', seller_status=False, buyer_status=False)

        # Convert the QuerySet to a list of dictionaries
        product_list = serializers.serialize('python', products)
        products = [{'pk': item['pk'], 'fields': item['fields']} for item in product_list]
        
        message_list = [{
            
            'products': products,
        }]

        return JsonResponse({
            'products': products,
        }, safe=False)


#CART CHECKOUT ORDER VIEW
@login_required(login_url = 'logout')    
def CartCheckOutView(request):
   
    if request.method == 'POST':
        
        #GET ALL SENT DATA, ADDRESS AND PAYEMENT MODE
        messagess = json.loads(request.body)
        payement_mode = messagess['payment_mode']
        address_code = messagess['address_code']
        
        address_code = Location.objects.get(pk = address_code)
        paid = messagess['paid']
        balance = messagess['balance']
        total_price = messagess['total_price']
        order_note = messagess['order_note']
       
        
        
        current_user = get_object_or_404(Profile,user_p = request.user)
        businesses = get_object_or_404(BusinessProfile,pk = (request.session['activebusiness']))
        
        last_order = CartOrders.objects.filter(source='ONLINE',order_product__category__cat__bar_cat =businesses,buyer_status = True,seller_status = True).order_by('-id')
        #get last order to assign an order number    
        if last_order:
            last_order = last_order[0]
            order_no = int(last_order.order_no)+1
            orders = CartOrders.objects.filter(source='ONLINE',order_by =current_user,buyer_status = False,seller_status = False)
            details = ', '.join(order.product_name+'('+order.quantity+')' for order in orders)
            
            Order_Summary.objects.create(
            customer = current_user,order_no=order_no,total=total_price,payement_mode = payement_mode,order_summary_business = businesses,
            balance = balance,order_note=order_note,code_address=address_code,paid = paid,source='ONLINE',details=details,order_status = 'Pending'
            )  
            
            
            for order in orders:
                current_stock = BarInventoryStock.objects.get(item__pk = order.order_product.pk)
                
                remaining_stock = int(current_stock.good)-int(order.quantity)
                print(current_stock.quantity_stocked_at_hand)
                remaining_stock_at_hand = current_stock.quantity_stocked_at_hand - int(order.quantity)
                current_stock.good = remaining_stock
                
                current_stock.quantity_stocked_at_hand = remaining_stock_at_hand
                    
                current_stock.save()
                
                orders.update(seller_status = True,buyer_status = True,order_no =order_no)
                message_list = [{
              
                        'message':'success',
              
                        }] 
                
            #save order summary 
              
                
            
        else:
            orders = CartOrders.objects.filter(source='ONLINE',order_by =current_user,buyer_status = False,seller_status = False)
            details = ', '.join(order.product_name+'('+order.quantity+')' for order in orders)
            
            Order_Summary.objects.create(
            customer = current_user,order_no=1,total=total_price,payement_mode = payement_mode,order_summary_business = businesses,
            balance = balance,order_note=order_note,code_address=address_code,paid = paid,source='ONLINE',details=details,order_status = 'Pending'
            )  
            
            
            for order in orders:
                current_stock = BarInventoryStock.objects.get(item__pk = order.order_product.pk)
                
                remaining_stock = int(current_stock.good)-int(order.quantity)
                print(current_stock.quantity_stocked_at_hand)
                remaining_stock_at_hand = current_stock.quantity_stocked_at_hand - int(order.quantity)
                current_stock.good = remaining_stock
                current_stock.quantity_stocked_at_hand = remaining_stock_at_hand
                current_stock.save()
                
              
            orders.update(seller_status = True,buyer_status = True,order_no =1)
            message_list = [{
      
                'message':'success',
      
                }]    
            #save order summary 
            
        
   
    return JsonResponse(message_list,safe=False)  

@login_required(login_url = 'logout')    
def SetCancelOrderView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        
        order_no = json.loads(request.body)
        request.session['cancelOrder'] = order_no
        
        
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)
    
@login_required(login_url = 'logout')    
def CancelOrderView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    if request.method == 'POST':
        ordersummary = Order_Summary.objects.get(pk = request.session['cancelOrder'])
        business = ordersummary.order_summary_business
        order_no = ordersummary.order_no
        order = Orders.objects.filter(order_product__business_p = business,order_by = current_user,order_no = order_no).delete()
        ordersummary.delete()
        
        
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)
    

@login_required(login_url = 'logout')    
def CalculateCartView(request):
   
    if request.method == 'POST':
        
        messagess = json.loads(request.body)
        
        item_id = messagess['itemid']
        newquantity = messagess['quantity']
        item = Orders.objects.get(pk=item_id)
        
        oldprice = item.price
        newprice =  Decimal(oldprice)*Decimal(newquantity)
        
        item.quantity = newquantity
        
        item.total_price = newprice
        item.save()
        current_user = get_object_or_404(Profile,user_p = request.user)
        carts = Orders.objects.filter(order_by =current_user,buyer_status = False)
        total_cost = 0
        for cart in carts:
            total_cost += cart.total_price
    
    message_list = [{
      
        'total_price':newprice,
        'newquantity':newquantity,
        'total_cost':total_cost,
        'grand_cost':total_cost,
      
    }]
   
    return JsonResponse(message_list,safe=False)   

 
    

        