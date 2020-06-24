class Product {

  int id;
  String name, company;

  Product();

  Product.fromMap(Map<String, dynamic> map) {
    this.id = map['id'];
    this.name = map['name'];
    this.company = map['company'];
  }

}