from django.urls import path
from . import views



urlpatterns = [
    path('', views.login, name='login'),
    path('billing', views.billing, name='billing'),
    path('stock', views.stock, name='stock'),
    path('report', views.report, name='report'),
    path('logout', views.logout, name='logout'),
]