from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(ProductBooking)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(ProductRequest)


