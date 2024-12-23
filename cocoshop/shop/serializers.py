# shop/serializers.py

from rest_framework import serializers
from .models import User, Products, Order, CartItems, Brands, Categories, Favourite, OrderItem
from .models import ChatRoom, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender_name', 'message', 'created_at', 'is_read']
        read_only_fields = ['is_read']

class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'created_at', 'updated_at', 'is_active', 'last_message', 'unread_count']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return ChatMessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        return obj.messages.filter(is_read=False).exclude(sender=obj.user).count()
    
    def create(self, validated_data):
        # Добавьте проверку или передайте user в validated_data
        validated_data['user'] = self.context['request'].user  # Убедитесь, что 'user' есть в контексте
        return super().create(validated_data)

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


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'email', 'phone', 'address', 
            'city', 'postal_code', 'shipping_notes', 'total_price', 
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_total_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total price must be greater than zero")
        return value

    def validate(self, data):
        # Ensure all required fields are present
        required_fields = ['full_name', 'email', 'phone', 'address', 'city', 'postal_code', 'total_price']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_brand = BrandsSerializer(source='product.brand', read_only=True)
    product_category = CategoriesSerializer(source='product.category', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)  # Explicitly map the product ID
    product_image = serializers.CharField(source='product.image_url', read_only=True)

    class Meta:
        model = Favourite
        fields = ['id', 'product_id', 'product_name', 'product_price', 'product_brand', 'product_category', 'product_image']


class CartItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_brand = BrandsSerializer(source='product.brand', read_only=True)
    product_category = CategoriesSerializer(source='product.category', read_only=True)
    product_image = serializers.CharField(source='product.image_url', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)  # Explicitly map the product ID

    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'product_name', 'product_price', 'quantity', 'product_brand', 'product_category',
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
