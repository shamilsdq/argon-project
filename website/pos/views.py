from django.shortcuts import render
from .models import Users, Products, Distributors, Stocks



def login(request):
    context = {}
    return render(request, 'pos/login.html', context)


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


def logout(request):
    pass