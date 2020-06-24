import 'dart:convert';
import 'package:flutterapp/models/product.dart';
import 'package:http/http.dart';
import 'package:location/location.dart';

import 'package:flutterapp/models/shop.dart';
import 'package:flutterapp/models/result.dart';


class APIService {

  final String baseurl = 'http://192.168.1.101:8000/api/';

  Future locateshops(int query, LocationData x) async {
    // String requestURL = "http://192.168.1.101:8000/api/?query=1&lat=9.454473&lon=76.436673";
    String requestURL = baseurl + ('?query=' + query.toString()) + ('&lat=' + x.latitude.toString()) + ('&lon=' + x.longitude.toString());
    print(requestURL);

    try {

      APIResult result = new APIResult();
      Response response = await get(requestURL);
      Map<String, dynamic> data = jsonDecode(response.body);

      if(data['error'].length != 0) {
        for(String error in data['error']) {
          result.errors.add(error);
        }
      }

      else {
        List<Shop> shops = new List();
        for(Map<String, dynamic> resultx in data['result']['shops']) {
          Shop shop = new Shop.fromMap(resultx);
          shops.add(shop);
        }
        result.shops = shops;
      }

      result.radius = data['result']['radius'];
      result.calculateZoom();

      print('API call was successful');
      return result;

    }

    catch(e) {
      print('API call gave an exception');
      return null;
    }

  }


  suggestions(String pattern) async {

    String requestURL = baseurl + 'suggest' + ('?query=' + pattern);
    print(requestURL);

    try {

      Response response = await get(requestURL);
      Map<String, dynamic> data = jsonDecode(response.body);

      if(data['error'].length != 0) throw ArgumentError.value('error');

      List<Product> products = new List();
      for(Map<String, dynamic> x in data['result']) {
        Product p = new Product.fromMap(x);
        products.add(p);
      }

      return products;

    }

    catch(e) {
      print("error occurred");
      return null;
    }


  }

}