from django.contrib import admin
from .models import Product, ProductCart, Profile, Order


admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(ProductCart)
admin.site.register(Order)
