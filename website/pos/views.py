from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pos.models import Users
from .models import Users, Products, Distributors, Stocks
from pos.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            newuser = form.save()
            newuser.refresh_from_db()  # load the profile instance created by the signal

            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            entry = Users.objects.create(name = name, address = address, latitude = latitude, longitude = longitude, user_id = newuser.id)
            entry.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = newuser.username, password = raw_password)
            login(request, user)
            return redirect(billing)

    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'pos/signup.html', context)


def signin(request):
    context = {}
    return render(request, 'pos/signin.html', context)


def signout(request):
    logout(request)
    return redirect(signin)


def billing(request):
    context = {}
    return render(request, 'pos/billing.html', context)


def stock(request):
    dbresult = Stocks.objects.filter(user__id=1).order_by('product_id')
    productlist = []
    for row in dbresult:
        ## passing a non-empty string to visible property will give true in js
        details = {'id': row.product_id, 'name': row.product.name, 'distributor': row.distributor.name, 'stock': row.stock, 'visible': '1'}
        productlist.append(details)
    context = {'productlist': productlist}
    return render(request, 'pos/stock.html', context)


def report(request):
    context = {}
    return render(request, 'pos/report.html', context)