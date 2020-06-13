from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from pos.models import Users
from .models import Users, Products, Distributors, Stocks
from pos.forms import SignUpForm


# ------------
# normal views
# ------------

def signup(request):

    if request.user.is_authenticated:
        return redirect(billing)

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            # Create an auth User.
            newuser = form.save()
            newuser.refresh_from_db()

            # Create a Users object with more details and link with auth User.
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            entry = Users.objects.create(name = name, address = address, latitude = latitude, longitude = longitude, user_id = newuser.id)
            entry.save()

            # Using these details, login the new user and go to billing page.
            password = form.cleaned_data.get('password1')
            user = authenticate(username = newuser.username, password = password)
            login(request, user)
            return redirect(billing)

    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'pos/signup.html', context)



def signin(request):

    if request.user.is_authenticated:
        return redirect(billing)
        
    if request.method == 'POST':
        form = AuthenticationForm(request = request, data = request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect(billing)
        
        messages.error(request, 'Invalid credentials')
    
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'pos/signin.html', context)



def signout(request):

    if request.user.is_authenticated:
        logout(request)

    return redirect(signin)



def billing(request):

    if request.user.is_authenticated:
        context = {}
        return render(request, 'pos/billing.html', context)

    else:
        return redirect(signin)



def stock(request):

    if request.user.is_authenticated:
        dbresult = Stocks.objects.filter(user__id=1).order_by('product_id')
        productlist = []

        for row in dbresult:
            ## passing a non-empty string to visible property will give true in js
            details = {'id': row.product_id, 'name': row.product.name, 'distributor': row.distributor.name, 'stock': row.stock, 'visible': '1'}
            productlist.append(details)

        context = {'productlist': productlist}
        return render(request, 'pos/stock.html', context)

    else:
        return redirect(signin)



def report(request):

    Products.objects.create(company="inglecorp", name="Sulphuric acid", genericname="hydrogen sulphide", mrp=80, tax=8)
    context = {}
    return render(request, 'pos/report.html', context)



def profile(request):
    pass



# --------------
# json responses
# --------------

def querynewproducts(request):

    if request.user.is_authenticated:
        data = {}
        word = request.GET.get('q', '')
        if word != '':
            data['query'] = word
        return JsonResponse(data)
    
    return redirect(signin)

    

def querystockproducts(request):
    
    if request.user.is_authenticated:
        data = {}
        return JsonResponse(data)
    
    return redirect(signin)