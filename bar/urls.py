from django.urls import path
from . import views


urlpatterns = [
   
    path('counter/',views.CounterView,name ='counter'),
    path('home/',views.HomeView,name ='home'),
    path('countercats/',views.CounterCatsView,name ='countercats'),
    path('counteritems/',views.CounterItemsView,name ='counteritems'),
    path('barstock/',views.BarStockView,name ='barstock'),
    path('barstocks/',views.BarStocksView,name ='barstocks'),
    
    path('newbarcategory/',views.CreateBarCategories,name ='newbarcategory'),
    path('ajaxaddbarsubcategory/',views.AjaxAddBarSubCategory,name ='ajaxaddbarsubcategory'),
    path('addbarsubcategory/',views.AddBarSubCategory,name ='addbarsubcategory'),
    
    path('newbaritem/',views.CreateBarItem,name ='newbaritem'),
    
    path('newbarstock/',views.CreateBarStock,name ='newbarstock'),
    path('newbarstockitem/',views.CreateBarStockItem,name ='newbarstockitem'),
    path('ajaxstock/',views.AjaxBarStock,name ='ajaxstock'),
    
    path('currentstock/',views.BarCurrentStock,name ='currentstock'),
    
    path('pos/',views.PointOfSale,name ='pos'),
    path('posonlineorders/',views.PointOfSaleOnlineOrders,name ='posonlineorders'),  
    path('posonlineordersajax/',views.PointOfSaleOnlineOrdersDetailsAjax,name ='posonlineordersajax'), 
    path('onlineorderteails/',views.OnlineOrderDetails,name ='onlineorderteails'), 
    path('placeonlineordertowaiter/',views.PlaceOnlineOrderToWaiter,name ='placeonlineordertowaiter'),
    
    path('posorders/',views.PointOfSaleOrders,name ='posorders'),
    path('myassignedposorders/',views.MyassignedPointOfSaleOrders,name ='myassignedposorders'),
    path('addtoposcart/',views.AddToPosCartView,name ='addtoposcart'), 
    path('removefromposcart/',views.RemoveFromPosCartView,name ='removefromposcart'),
    path('changeqtyposcart/',views.ChangeQtyFromPosCartView,name ='changeqtyposcart'),
    path('poscheckout/',views.PosCheckOutView,name ='poscheckout'), 
    path('orderstatus/',views.OrderStatusView,name ='orderstatus'),
    path('changeorderstatus/',views.ChangeOrderStatusView,name ='changeorderstatus'),  
    path('setcategory/',views.SetCategoryView,name ='setcategory'),
    path('changeorderstatusajax/',views.ChangeOrderStatusAjaxView,name ='changeorderstatusajax'), 
    
    path('addtocart/',views.AddtoCartView,name ='addtocart'), 
    path('countercart/',views.CounterCartView,name ='countercart'), 
    path('removefromcountercart/',views.RemoveFromCounterCartView,name ='removefromcountercart'),
    path('changeqtycountercart/',views.ChangeQtyFromCounterCartView,name ='changeqtycountercart'),
    path('cartcheckout/',views.CartCheckOutView,name ='cartcheckout'),
    path('myorders/',views.MyOrdersView,name ='myorders'),
    path('myordersdetailsajax/',views.MyOrdersDetailsAjaxView,name ='myordersdetailsajax'),
    path('myordersdetails/',views.MyOrdersDetailsView,name ='myordersdetails'),
    path('trackorder/',views.TrackCounterOrderView,name ='trackorder'),
]