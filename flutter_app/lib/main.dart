import 'package:flutter/material.dart';
import 'package:flutterapp/screens/homepage.dart';

void main() => runApp(Argon());

class Argon extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: Color(0xffFFFFFF),
        appBarTheme: AppBarTheme(
          elevation: 0.0,
          color: Color(0xffFFFFFF),
          textTheme: TextTheme(
            headline6: TextStyle(
              color: Colors.black,
              fontSize: 17.0,
              letterSpacing: 3.0,
            ),
          ),
          iconTheme: IconThemeData(
            color: Color(0xffFFFFFF),
          ),
        ),
        buttonTheme: ButtonThemeData(
          buttonColor: Color(0xff273952),
          padding: EdgeInsets.symmetric(vertical: 15.0, horizontal: 35.0),
          shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(25.0)
          ),
          textTheme: ButtonTextTheme.primary,
        ),
        inputDecorationTheme: InputDecorationTheme(
          contentPadding: EdgeInsets.symmetric(vertical: 15.0, horizontal: 23.0),
          fillColor: Color(0xffEEEEF5),
          focusColor: Color(0xffFFFFFF),
          filled: true,
          hintStyle: TextStyle(
            color: Colors.blueGrey,
            fontSize: 18.0,
          ),
          suffixStyle: TextStyle(
            color: Colors.black,
            fontSize: 18.0,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(25.0),
            borderSide: BorderSide(
              color: Color(0x99cccccc),
              width: 0.0,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(25.0),
            borderSide: BorderSide(
              color: Color(0xff273952),
              width: 1.0,
            ),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(25.0),
            borderSide: BorderSide(
              color: Color(0xffff0000),
              width: 1.0,
            ),
          ),
        ),
        textTheme: TextTheme(
          bodyText2: TextStyle(
            color: Colors.white,
            fontSize: 17.0,
          ),
          button: TextStyle(
            color: Colors.white,
            fontSize: 17.0,
            fontWeight: FontWeight.w300,
            letterSpacing: 1.0,
          ),
        ),
      ),
      title: 'Argon - Find medicines nearby',
      home: Home(),
    );
  }
}