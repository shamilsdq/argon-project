import math
from django.http import JsonResponse, HttpResponse
from pos.models import Users, Products, Stocks
from django.db.models.expressions import RawSQL





# api request to get product details as suggestion
def suggest(request):
     
    data = {'error': [], 'result': []}
    query = request.GET.get('query')

    # check for errors in api call
    if query is None:
        data['error'].append('no query')
        
    # if no errors, get data
    if data['error'] == []:
        
        products = Products.objects.filter(name__contains = query) | Products.objects.filter(company__startswith = query)
        products = products.values('id', 'company', 'name')
        for product in products:
            data['result'].append(product)

    return JsonResponse(data)
    




# handle api requests
def apicall(request):
    
    data = {'error': [], 'result': None}
    query = request.GET.get('query')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    # check for errors in api call
    if query is None:
        data['error'].append('Invalid product')
    if lat is None or lon is None:
        data['error'].append('Invalid location data')

    # if no errors, get data
    if data['error'] == []:

        lat = float(lat)
        lon = float(lon)

        if Products.objects.filter(id = query).count != 0:
            data['result'] = findshops(query, lat, lon, 3)

    return JsonResponse(data)





# recursive function for apicall
def findshops(query, lat, lon, r=3):

    result = {'shops': [], 'radius': r}

    if r >= 200:
        return result

    minLat, maxLat = lat - math.degrees(r/6371), lat + math.degrees(r/6371)
    minLon = lon - math.degrees(math.asin(r/6371) / math.cos(math.radians(lat)))
    maxLon = lon + math.degrees(math.asin(r/6371) / math.cos(math.radians(lat)))

    users = Users.objects.raw('SELECT * FROM pos_users WHERE id IN (SELECT user_id FROM pos_stocks WHERE product_id = %s AND STOCK > 0) HAVING latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s', [query, minLat, maxLat, minLon, maxLon])
    for user in users:
        x = {'id': user.id, 'name': user.name, 'address': user.address, 'latitude': user.latitude, 'longitude': user.longitude}
        result['shops'].append(x)

    if result['shops'] == []:
        result = findshops(query, lat, lon, r*2)

    return result