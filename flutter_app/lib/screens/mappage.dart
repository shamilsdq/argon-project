import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutterapp/services/maputils.dart';

import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';

import 'dart:typed_data';
import 'dart:ui' as ui;
import 'dart:async';

import 'package:flutterapp/widgets/loading.dart';
import 'package:flutterapp/models/shop.dart';
import 'package:flutterapp/models/product.dart';
import 'package:flutterapp/models/result.dart';
import 'package:flutterapp/services/api.dart';



class MapPage extends StatefulWidget {
  final Product product;
  MapPage({ this.product });

  @override
  _MapPageState createState() => _MapPageState();
}



class _MapPageState extends State<MapPage> {

  Completer<GoogleMapController> _mapcontroller = Completer();
  GoogleMapController _controller;
  Location _location = new Location();
  LocationData _startLocation, _currentLocation;
  StreamSubscription<LocationData> _locationSubscription;

  Marker myMarker = Marker(markerId: MarkerId('me'), position: LatLng(0, 0));
  Set<Marker> markers = Set();
  Set<Circle> circles = Set();
  double mapZoom = 15.0;


  @override
  void initState() {
    super.initState();
    initPlatformState();
  }


  @override
  void dispose() {
    if(_locationSubscription != null) _locationSubscription.cancel();
    super.dispose();
  }


  @override
  Widget build(BuildContext context) {
    return _startLocation == null ?
    Loading() : Scaffold(
      body: Stack(
        children: <Widget>[
          GoogleMap(
            onMapCreated: (GoogleMapController controller){
              _setStyle(controller);
              _mapcontroller.complete(controller);
              _controller = controller;
            },
            initialCameraPosition: CameraPosition(
              target: LatLng(_currentLocation.latitude, _currentLocation.longitude),
              zoom: mapZoom,
            ),
            markers: markers,
            circles: circles,
          ),
        ],
      ),
    );
  }


  /* if permitted get startlocation and the subscribe to listen to location changes */
  initPlatformState() async {

    final Uint8List myMarkerIcon = await getBytesFromAsset('assets/myicon.png', 40);
    final Uint8List shopMarkerIcon = await getBytesFromAsset('assets/markericon.png', 60);

    LocationData location;
    if(await _location.hasPermission() == PermissionStatus.GRANTED) {

      _locationSubscription = _location.onLocationChanged()
          .listen((LocationData result) {

              _currentLocation = result;

              setState(() {
                markers.remove(myMarker);
                myMarker = Marker(
                  markerId: MarkerId('ME'),
                  position: LatLng(_currentLocation.latitude, _currentLocation.longitude),
                  icon: BitmapDescriptor.fromBytes(myMarkerIcon),
                );
                markers.add(myMarker);
              });

              if(_startLocation == null) {
                _startLocation = _currentLocation;
                updateShops(shopMarkerIcon);
              }

          });

      /*markers.addAll([
        Marker(
          markerId: MarkerId('cucek'),
          position: LatLng(9.460568, 76.438183),
          icon: BitmapDescriptor.fromBytes(shopMarkerIcon),
          anchor: Offset(0.0, 0.75),
          infoWindow: InfoWindow(
              title: 'cucek medicals',
              onTap: () {
                Navigator.pop(context);
              }
          ),
        ),
        Marker(
          markerId: MarkerId('test1'),
          position: LatLng(9.460050, 76.445183),
          icon: BitmapDescriptor.fromBytes(shopMarkerIcon),
          onTap: () {},
        ),
        Marker(
          markerId: MarkerId('test2'),
          position: LatLng(9.451050, 76.445183),
          icon: BitmapDescriptor.fromBytes(shopMarkerIcon),
          onTap: () {},
        ),
        Marker(
          markerId: MarkerId('test2'),
          position: LatLng(9.450050, 76.435183),
          icon: BitmapDescriptor.fromBytes(shopMarkerIcon),
          onTap: () {},
        ),
      ]);*/

    } else {

      PermissionStatus _permission = await _location.requestPermission();
      if(_permission != PermissionStatus.GRANTED) Navigator.pop(context);

    }

  }

  void updateShops(Uint8List shopMarkerIcon) async {
    print('calling api');
    APIResult result = await APIService().locateshops(widget.product.id, _startLocation);
    if(result == null) {
      print('api returned null');
      return;
    }
    if(result.errors != null) {
      print('error in API call');
      return;
    }
    mapZoom = result.zoom;

    if(_controller != null){
      _controller.animateCamera(CameraUpdate.newLatLngZoom(
        LatLng(_currentLocation.latitude, _currentLocation.longitude),
        mapZoom,
      ));
    }

    for(Shop shopx in result.shops){
      print(shopx.name);
      bool flag = false;
      for(Marker markerx in markers) {
        if(markerx.markerId == shopx.id.toString()) {
          flag = true;
          break;
        }
      }
      if(flag == false) {
        Marker m = new Marker(
          markerId: MarkerId(shopx.id.toString()),
          position: shopx.location,
          icon: BitmapDescriptor.fromBytes(shopMarkerIcon),
          infoWindow: InfoWindow(
              title: shopx.name,
              snippet: shopx.address,
              onTap: () {
                MapUtils.openMap(shopx.location.latitude, shopx.location.longitude);
              }
          ),
        );
        setState(() {
          markers.add(m);
        });
      }
    }
  }


  Future<Uint8List> getBytesFromAsset(String path, int width) async {
    ByteData data = await rootBundle.load(path);
    ui.Codec codec = await ui.instantiateImageCodec(data.buffer.asUint8List(), targetWidth: width);
    ui.FrameInfo fi = await codec.getNextFrame();
    return (await fi.image.toByteData(format: ui.ImageByteFormat.png)).buffer.asUint8List();
  }

  void _setStyle(GoogleMapController controller) async {
    String value = await DefaultAssetBundle.of(context)
        .loadString('assets/mapstyle.json');
    controller.setMapStyle(value);
  }

}