import 'package:flutter/material.dart';
import 'package:flutterapp/screens/mappage.dart';


class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  GlobalKey<FormState> _searchform = GlobalKey<FormState>();
  String _searchtext = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ARGON'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Center(
          child: Form(
            key: _searchform,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                TextFormField(
                    decoration: InputDecoration(
                      hintText: 'Medicine Name',
                    ),
                    onChanged: (val) => _searchtext = val,
                    validator: (val) {
                      if(val.isEmpty) return 'Empty';
                      return null;
                    }
                ),
                SizedBox(height: 20.0),
                RaisedButton(
                  child: Text('Find availability'),
                  elevation: 5.0,
                  onPressed: () {
                    if(_searchform.currentState.validate()) {
                      Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => MapPage(searchtext: _searchtext))
                      );
                    }
                    else {
                      Scaffold.of(context)
                          .showSnackBar(SnackBar(content: Text('Empty search string')));
                    }
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}