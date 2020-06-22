from django.urls import path
from . import views



urlpatterns = [
    path('suggest', views.suggest, name='suggest'),
    path('', views.apicall, name='apicall'),
]
