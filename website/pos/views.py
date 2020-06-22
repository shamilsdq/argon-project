from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from pos.forms import SignUpForm

from django.db import transaction
from .models import Users, Products, Stocks, Bills, BillItems
import json

# --------------------
# normal views section
# --------------------

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

    return redirect(signin)



def report(request):

    if request.user.is_authenticated:
        context = {}
        return render(request, 'pos/report.html', context)

    return redirect(signin)



#def profile(request):
#
#    if request.user.is_authenticated:
#        context = {}
#        return render(request, 'pos/profile.html', context)
#
#    return redirect(signin)



# -------------------
# async calls section
# -------------------

def querynewproducts(request):

    if request.user.is_authenticated:
        data = {}
        word = request.GET.get('q', '')

        if word != '':
            data['query'] = word
            nameset = Products.objects.filter(name__startswith = word)
            companyset = Products.objects.filter(company__startswith = word)
            genericset = Products.objects.filter(genericname__startswith = word)
            productset = nameset | companyset | genericset
            result = []

            for product in productset:
                x = {'id': product.id, 'name': product.name, 'company': product.company, 'genericname': product.genericname, 'mrp': product.mrp, 'tax': product.tax}
                result.append(x)

            data['result'] = result 

        else:
            data['query'] = None
            data['result'] = None

        return JsonResponse(data)
    
    return redirect(signin)

    

def querystockproducts(request):
    
    if request.user.is_authenticated:
        data = {}
        word = request.GET.get('q', '')

        if word != '':
            data['query'] = word
            productset = Stocks.objects.filter(user = request.user).filter(product__name__startswith = word)
            result = []

            for product in productset:
                if product.stock <= 0: continue
                x = {'id': product.product_id, 'name': product.product.name, 'mrp': product.product.mrp, 'price': product.price}
                result.append(x)
            
            data['result'] = result
            
        else:
            data['query'] = None
            data['result'] = None
            
        return JsonResponse(data)
    
    return redirect(signin)



def savebill(request):

    if request.user.is_authenticated:
        result = {'status': 'Processing'}

        try:
            with transaction.atomic():
                billdata = json.loads(request.body.decode('utf-8')) 
                bill = Bills.objects.create(
                    user = request.user,
                    customernumber = billdata['customernumber'],
                    amount = billdata['amount'],
                    ispaid = True
                )

                for item in billdata['billitems']:
                    BillItems.objects.create(
                        bill = bill,
                        product = item['id'],
                        quantity = item['quantity']
                    )   

                result['status'] = 'Success'

        except:
            result['status'] = 'Failure'
            
        return JsonResponse(result)
    
    return redirect(signin)