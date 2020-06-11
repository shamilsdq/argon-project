from django.db import models



class Users(models.Model):

    id = models.AutoField(primary_key = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50)
    name = models.CharField(max_length = 40)
    address = models.TextField(max_length = 80)
    latitude = models.DecimalField(max_digits = 9, decimal_places = 6)
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6)
    creation = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.name
    


class Products(models.Model):

    id = models.AutoField(primary_key = True)
    company = models.CharField(max_length = 50)
    name = models.CharField(max_length = 40)
    genericname = models.CharField(max_length = 75)
    mrp = models.FloatField()
    tax = models.FloatField()

    def __str__(self):
        return self.company + ' ' + self.name
    


class Distributors(models.Model):

    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 40)
    number = models.IntegerField()
    address = models.TextField(max_length = 80)

    def __str__(self):
        return self.name



class Stocks(models.Model):

    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    distributor = models.ForeignKey(Distributors, on_delete = models.CASCADE)
    cost = models.FloatField()
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.product.name + ': ' + str(self.stock)
    


class Bills(models.Model):

    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now = True)
    customernumber = models.IntegerField()
    amount = models.FloatField()
    ispaid = models.BooleanField()

    def __str__(self):
        return self.customernumber + ": " + self.amount
    


class BillItems(models.Model):

    bill = models.ForeignKey(Bills, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product + ": " + self.quantity
    