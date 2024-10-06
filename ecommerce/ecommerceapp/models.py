from django.db import models
from django.contrib import admin

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default='')
    message = models.TextField(default='') 

    def __str__(self):
        return self.name  

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name
    
class Order(models.Model):
   order_id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=100)
   email = models.EmailField(default="")
   address1 = models.CharField(max_length=255)
   address2 = models.CharField(max_length=255, blank=True, null=True)
   city = models.CharField(max_length=100)
   state = models.CharField(max_length=100)
   zipcode = models.CharField(max_length=20)
   phone = models.CharField(max_length=15)
   total_amount = models.CharField(max_length=100)
   payment_id = models.CharField(max_length=100, blank=True, null=True)  # PayPal Payment ID
   status = models.CharField(max_length=20, default="Pending")

def __str__(self):
        return self.name
class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
