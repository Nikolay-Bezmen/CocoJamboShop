# shop/serializers.py

from rest_framework import serializers
from .models import User, Products, Order, CartItems, Brands, Categories


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description']


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandsSerializer(read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'brand', 'category', 'image_url']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_brand = BrandsSerializer(source='product.brand', read_only=True)
    product_category = CategoriesSerializer(source='product.category', read_only=True)

    class Meta:
        model = CartItems
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'product_brand', 'product_category']
