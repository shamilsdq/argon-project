from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from pos.forms import SignUpForm

from django.db import transaction
from .models import *
import json
import datetime



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

        productlist = []
        dbresult = Stocks.objects.filter(user__id = request.user.id).order_by('product_id')

        for row in dbresult:
            ## passing a non-empty string to visible property will give true in js
            details = {'id': row.product_id, 'name': row.product.name, 'distributor': row.distributor.name, 'stock': row.stock, 'visible': '1'}
            productlist.append(details)

        distributorlist = []
        dbresult = Distributors.objects.raw('SELECT * FROM pos_distributors WHERE id IN (SELECT distributor_id FROM pos_stocks WHERE user_id = %s)', [request.user.id])

        for row in dbresult:
            details = {'id': row.id, 'name': row.name}
            print(row.name)
            distributorlist.append(details)

        context = {'productlist': productlist, 'distributorlist': distributorlist}
        return render(request, 'pos/stock.html', context)

    return redirect(signin)



def report(request):

    if request.user.is_authenticated:
        context = {}

        report_week = {'sale': 0, 'bills': 0}
        bills = Bills.objects.raw('SELECT * FROM pos_bills WHERE user_id = %s AND time > %s', [request.user.id, datetime.datetime.now() - datetime.timedelta(days=7)])
        for x in bills:
            report_week['sale'] += x.amount
            report_week['bills'] += 1

        report_today = {'sale': 0, 'bills': 0}
        bills = Bills.objects.raw('SELECT * FROM pos_bills WHERE user_id = %s AND CAST(time AS DATE) = %s', [request.user.id, datetime.date.today()])
        for x in bills:
            report_today['sale'] += x.amount
            report_today['bills'] += 1

        all_bills = []
        dbresult = Bills.objects.filter(user_id = request.user.id)
        for row in dbresult:
            x = {'id': row.id, 'contact': row.customernumber, 'amount': row.amount, 'visible': '1'}
            print(x)
            all_bills.append(x)

        context['week'] = report_week
        context['today'] = report_today
        context['bills'] = all_bills

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
            productset = Stocks.objects.filter(user = request.user.id).filter(product__name__startswith = word)
            result = []

            for product in productset:
                if product.stock <= 0: continue
                x = {'id': product.product_id, 'name': product.product.name, 'mrp': product.product.mrp, 'price': product.price, 'qty': 1}
                result.append(x)
            
            data['result'] = result
            
        else:
            data['query'] = None
            data['result'] = None
            
        return JsonResponse(data)
    
    return redirect(signin)



def billdetails(request):
    
    if request.user.is_authenticated:
        data = {}
        word = request.GET.get('q', 0)

        if word != 0:
            word = int(word)
            data['query'] = word
            billitems = BillItems.objects.filter(bill_id = word)
            result = []

            for item in billitems:
                x = {'product': item.product.name, 'quantity': item.quantity}
                result.append(x)

            data['result'] = result

        else:
            data['query'] = data['result'] = None

        return JsonResponse(data)
    
    return redirect(signin)



def savebill(request):

    if request.user.is_authenticated:
        result = {}
        billform = json.loads(request.body)
        if int(billform['contact']) > 9999999999 or billform['items'] == [] or float(billform['amount']) <= 0:
            raise ValueError

        try:
            with transaction.atomic():
            
                print('checkpoint 1')
                bill = Bills.objects.create(
                    user = Users.objects.get(id = request.user.id),
                    customernumber = int(billform['contact']),
                    amount = float(billform['amount']),
                    ispaid = True
                )
                print('checkpoint 2')
                for item in billform['items']:
                    BillItems.objects.create(
                        bill = bill,
                        product = Products.objects.get(id = item['id']),
                        quantity = item['qty'],
                    )
                print('checkpoint 3')

            result = {'process': 'Success'}
        
        except:
            result = {'process': 'Failure'}
            
        return JsonResponse(result)
    
    return redirect(signin)



def addstock(request):
    
    if request.user.is_authenticated:
        result = {}
        form = json.loads(request.body)
        print(form)

        try:
            stock = Stocks.objects.filter(user_id = request.user.id).filter(product_id = int(form['productid']))
            
            # if it is a new product
            if not stock:
                Stocks.objects.create(
                    user = Users.objects.get(id = request.user.id),
                    product = Products.objects.get(id = int(form['productid'])),
                    distributor = Distributors.objects.get(id = int(form['distributorid'])),
                    cost = float(form['cost']),
                    price = float(form['price']),
                    stock = int(form['stock']),
                )
                result['process'] = 'New stock created'

            # else update old stock
            else:
                for x in stock:
                    x.stock += int(form['stock'])
                    x.cost = float(form['cost'])
                    x.price = float(form['price'])
                    x.save()
                    break
                result['process'] = 'Stock updated'

        except:
            result['process'] = 'Failure'


        return JsonResponse(result)
    
    return redirect(signin)