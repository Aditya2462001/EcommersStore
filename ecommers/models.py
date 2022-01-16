from django.db import models
from django.db.models import base
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
from django.utils import tree
from django.utils.text import slugify

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True,blank=True)
    number = models.CharField(max_length=12,null=True,blank=True)
    email = models.EmailField(max_length=256,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='customer',null=True,blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=5000,null=True,blank=True)
    image = models.ImageField(upload_to='category-img/', null=True,blank=True)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    product_name = models.CharField(max_length=500,null=True,blank=True)
    product_slug = models.SlugField(null=True,blank=True)
    product_desc = models.TextField(null=True,blank=True)
    product_feature = models.TextField(null=True,blank=True)
    product_rating = models.IntegerField(null=True,blank=True)
    rate = models.IntegerField(null=True,blank=True)
    selling_rate =  models.IntegerField(null=True,blank=True)
    stock_count = models.IntegerField(null=True,blank=True)
    available = models.BooleanField(default=True,blank=True,null=True)
    product_date = models.DateField(auto_now=False, auto_now_add=True)
    product_image1 = models.ImageField(upload_to='productImages/',null=True, blank=True)
    product_image2 = models.ImageField(upload_to='productImages/',null=True, blank=True)
    product_image3 = models.ImageField(upload_to='productImages/',null=True, blank=True)
    product_image4 = models.ImageField(upload_to='productImages/',null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)


    def save(self, *args, **kwargs):
        self.product_slug = slugify(self.product_name)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_cost = models.CharField(max_length=50,null=True,blank=True)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer)
    

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products ,on_delete=models.CASCADE)
    content = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return str(self.product)
    

class ProductBooking(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart,blank=True)
    name = models.CharField( max_length=1000,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    number = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=500,null=True,blank=True)
    pincode = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    total_amount = models.IntegerField(null=True,blank=True)

    payment_type = models.CharField(max_length=500,null=True,blank=True)

    booking_id = models.CharField(max_length=50,null=True,blank=True)
    booking_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    delivary_status = models.CharField(max_length=1000,null=True,blank=True)
    booking_status = models.BooleanField(default=False,null=True,blank=True)

    razorpay_orderId = models.CharField(max_length=10000,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=1000,null=True,blank=True)
    payment_status = models.CharField(max_length=1000,null=True,blank=True)


    def save(self, *args, **kwargs):
        if not self.booking_id and self.booking_date and self.id:
            self.booking_id = self.booking_date.strftime('PAY2ME%Y%m%dORD')+str(self.id)
        super(ProductBooking, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.customer)

class ProductRequest(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=1000,null=True,blank=True)
    product_name = models.TextField(null=True,blank=True)
    product_id = models.CharField(max_length=50000,null=True,blank=True)
    defect_info = models.TextField(null=True,blank=True)
    request_action = models.CharField(max_length=100,null=True,blank=True)
    accept_message = models.CharField(max_length=1000,null=True,blank=True)
    return_payment = models.CharField(max_length=5000,null=True,blank=True)


    def __str__(self):
        return str(self.booking_id)
    
    

    
