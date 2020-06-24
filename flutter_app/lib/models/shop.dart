import 'package:google_maps_flutter/google_maps_flutter.dart';

class Shop {
  int id;
  String name, address;
  LatLng location;

  Shop.fromMap(Map<String, dynamic> map) {
    print("in shop model");
    this.id = map['id'];
    this.name = map['name'];
    this.address = map['address'];
    this.location = new LatLng(double.parse(map['latitude']), double.parse(map['longitude']));
  }
}