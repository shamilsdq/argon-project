import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';
import 'dart:async';
import 'package:flutterapp/widgets/loading.dart';

class MapPage extends StatefulWidget {
  final String searchtext;
  MapPage({ this.searchtext });

  @override
  _MapPageState createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  Completer<GoogleMapController> _mapcontroller = Completer();
  Location _location = new Location();

  LocationData _startLocation, _currentLocation;
  StreamSubscription<LocationData> _locationSubscription;

  @override
  void initState() {
    super.initState();
    initPlatformState();
  }

  @override
  void dispose() {
    _locationSubscription.cancel();
    super.dispose();
  }

  initPlatformState() async {
    LocationData location;
    try {
      location = await _location.getLocation();
      _locationSubscription = _location.onLocationChanged().listen(
              (LocationData result){
            setState(() => _currentLocation = result);
          });
    } on PlatformException catch(e) {
      if (e.code == 'PERMISSION_DENIED') {
        Navigator.pop(context);
      } else if (e.code == 'PERMISSION_DENIED_NEVER_ASK') {
        Navigator.pop(context);
      }
      location = null;
    }
    setState(() => _startLocation = location);
  }

  Set<Marker> markers = Set();

  @override
  Widget build(BuildContext context) {
    markers.addAll([
      Marker(
          markerId: MarkerId('micheals'),
          position: LatLng(9.448286, 76.435277)),
      Marker(
          markerId: MarkerId('carmel'),
          position: LatLng(9.448952, 76.439914)),
    ]);
    return _startLocation == null ?
    Loading() : Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blueGrey[400],      ),
      body: Stack(
        children: <Widget>[
          GoogleMap(
            onMapCreated: (GoogleMapController controller){
              _mapcontroller.complete(controller);
            },
            initialCameraPosition: CameraPosition(
              target: LatLng(_currentLocation.latitude, _currentLocation.longitude),
              zoom: 18.0,
            ),
            markers: markers,
          ),
        ],
      ),
    );
  }
}