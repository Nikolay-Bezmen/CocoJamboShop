from django.contrib import admin
from .models import Categories, Brands, Products, Carts, CartItems
admin.site.register(Categories)
admin.site.register(Brands)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(CartItems)

