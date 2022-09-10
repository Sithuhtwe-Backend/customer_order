import imp
from operator import mod
from secrets import choice
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ImageField(null=True, blank = True, upload_to="static/profiles")
    
    def __str__(self):
        return self.name

#need to specify fieldname and app name at begining 
#python manage.py makemigrations --name changed_my_model your_app_label


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    Category = [
        ('in door',"In Door"),
        ('out door',"Out Door")
    ]
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=Category)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    #key and values must be the same
    status_choice = [
        ('pd',"Pending"),
        ('ofd',"Out For Delivery"),
        ('d',"Delivered")
    ]
    #if you want to set on_delete as Null, you have to add null=True, blank=True
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=status_choice)
    
    def __str__(self) -> str:
        return self.product.name