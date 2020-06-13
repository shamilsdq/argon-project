from django.urls import path
from . import views



urlpatterns = [

    path('', views.signin, name='signin'),
    path('logout', views.signout, name='logout'),
    path('signup', views.signup, name='signup'),
    
    path('billing', views.billing, name='billing'),
    path('stock', views.stock, name='stock'),
    path('report', views.report, name='report'),

]