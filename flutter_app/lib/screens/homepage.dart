import 'package:flutter/material.dart';
import 'package:flutter_typeahead/flutter_typeahead.dart';
import 'package:flutterapp/models/product.dart';

import 'package:flutterapp/screens/mappage.dart';
import 'package:flutterapp/services/api.dart';


class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  GlobalKey<FormState> _searchform = GlobalKey<FormState>();
  String _searchtext = '';
  Product selectedProduct;
  TextEditingController _controller = new TextEditingController();

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
                TypeAheadField(

                  textFieldConfiguration: TextFieldConfiguration(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Search medicine',
                    ),
                  ),

                  suggestionsCallback: (pattern) async {
                    if(pattern.length == 0) return null;
                    return await APIService().suggestions(pattern);
                  },

                  suggestionsBoxDecoration: SuggestionsBoxDecoration(
                    color: Color(0xcc29cc9f),
                    borderRadius: BorderRadius.circular(15),
                  ),

                  itemBuilder: (context, product) {
                    return ListTile(
                      title: Text(product.name),
                    );
                  },

                  onSuggestionSelected: (product) {
                    selectedProduct = product;
                    this._controller.text = product.name;
                  },
                  hideOnLoading: true,
                ),
                SizedBox(height: 20.0),
                Builder(
                  builder: (BuildContext context) {
                    return RaisedButton(
                      child: Text('Find availability'),
                      elevation: 5.0,
                      onPressed: () {
                        if(selectedProduct != null) {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => MapPage(product: selectedProduct)),
                          );
                        }
                        else {
                          Scaffold.of(context)
                              .showSnackBar(SnackBar(content: Text('No such product')));
                        }
                      },
                    );
                  },
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}