from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [

    path('', views.signin, name='signin'),
    path('logout', views.signout, name='logout'),
    path('signup', views.signup, name='signup'),

    #path('profile', views.profile, name='profile'),
    
    path('billing', views.billing, name='billing'),
    path('savebill', csrf_exempt(views.savebill), name='savebill'),
    path('stock', views.stock, name='stock'),
    path('addstock', csrf_exempt(views.addstock), name='addstock'),
    path('report', views.report, name='report'),

    path('query/newproducts', views.querynewproducts, name='newproductsquery'),
    path('query/stockproducts', views.querystockproducts, name='stockproductsquery'),
    path('query/billdetails', views.billdetails, name='billdetailsquery'),

]