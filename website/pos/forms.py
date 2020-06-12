from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):

    name = forms.CharField(max_length = 40)
    address = forms.CharField(max_length = 80)
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'address', 'latitude', 'longitude')