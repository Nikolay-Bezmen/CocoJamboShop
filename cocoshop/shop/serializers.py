# shop/serializers.py

from rest_framework import serializers
from .models import User, Products, Order, CartItems, Brands, Categories, Favourite


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


class FavouriteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_brand = BrandsSerializer(source='product.brand', read_only=True)
    product_category = CategoriesSerializer(source='product.category', read_only=True)

    class Meta:
        model = Favourite
        fields = ['id', 'product', 'product_name', 'product_price', 'product_brand', 'product_category']


class CartItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_brand = BrandsSerializer(source='product.brand', read_only=True)
    product_category = CategoriesSerializer(source='product.category', read_only=True)
    product_image = serializers.CharField(source='product.image_url', read_only=True)

    class Meta:
        model = CartItems
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'product_brand', 'product_category',
                  'product_image']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
