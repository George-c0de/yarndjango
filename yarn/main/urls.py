from django.urls import path,include
from .import views

urlpatterns = [
    path('addtocartdefaultapp/',views.add_to_cart_default_app,name='add_to_cart_default_app'),
    # path('masterclassorderapp/',views.masterclassorderapp,name='masterclassorderapp'),
    path('orderpostapp/',views.orderpostapp,name='orderpostapp'),
    path('commentorderapp/',views.commentorderapp,name='commentorderapp'),
    path('getuserphone/',views.get_user_phone,name='getuserphone'),
    path('getuserorderactive/',views.get_user_order_active,name='get_user_order_active'),
    path('confirmpromocodeapp/',views.confirmpromocode_app,name='confirmpromocode_app'),
    path('gettotalcart/',views.get_total_cart,name='get_total_cart'),
    path('getloggin/',views.get_loggin,name='get_loggined'),
    
    path('checkloggined/',views.check_loggined,name='get_loggined'),
    path('checklogginedcart/',views.check_loggined_cart,name='get_loggined'),


    path('sendcode/',views.send_code_app,name='sendcode'),
    path('registeruser/',views.register_user,name='registeruser'),
    path('checkuser/',views.check_user,name='checkuser'),
    path('logout/',views.logout,name='logout'),
    path('promocodetocart/',views.promocode_to_cart,name='promocode_to_cart'),
    path('checkpromocade/',views.checkpromocade,name='checkpromocade'),
    path('checkaddressin/',views.check_address_in,name='check_address_in'),
    path('checkaddressanswer/',views.check_address_answer,name='check_address_answer'),
    # path('cart/',views.cart,name='cart'),
    path('saveaddress/',views.saveaddress,name='saveaddress'),
    path('addtocartapp/',views.add_to_cart_product_app,name='add_to_cart_product_app'),
    path('delfromcartapp/',views.del_from_cart_app,name='del_from_cart_app'),
    path('delfromcartdefaultapp/',views.del_from_cart_default_app,name='del_from_cart_default_app'),
    path('changeitemcartapp/',views.change_item_cart_app,name='change_item_cart_app'),
    path('changeitemcartdefaultapp/',views.change_item_cart_default_app,name='change_item_cart_default_app'),
    # path('loginsend/',views.login_number,name='login_number'),
    # path('loginuser/',views.login_user,name='login_user'),
    path('confirmpromocode/',views.confirmpromocode_app,name='confirmpromocode'),
    path('cartproducts/', views.cart_products,name='cart_products'),
    path('getpolicy/',views.getpolicy,name='getpolicy'),
    path('getabout/',views.getabout,name='getabout'),

    path('savename/',views.savename,name='savename'),
    path('saveemail/',views.saveemail,name='saveemail'),
    path('savebirthday/',views.savebirthday,name='savebirthday'),
    path('savepush/',views.savepush,name='savepush'),

    path('pickupchange/',views.pickup_change,name='pickup_change'),
    path('deliverychoise/',views.delivery_choise,name='delivery_choise'),
    path('pickupchoice/',views.pickup_choice,name='pickup_choice'),
    
    path('createorderpickup/',views.createorderpickup,name='createorderpickup'),

]