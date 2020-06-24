import 'dart:math';
import 'package:flutterapp/models/shop.dart';

class APIResult {

  int radius;
  List<String> errors;
  List<Shop> shops;
  double zoom;

  APIResult();

  calculateZoom(){
    zoom = 16 - (log(radius*2) / log(2));
  }

}