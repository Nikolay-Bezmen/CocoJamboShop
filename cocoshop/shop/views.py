# views.py

from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound, JsonResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from shop.forms import UserRegistrationForm
from shop.models import User, Products, CartItems, Favourite
from shop.serializers import (
    UserSerializer, CartItemsSerializer, ProductSerializer, 
    FavouriteSerializer
)
from shop.services.cartoperations import get_or_create_cart
from django.db import models
import json

# views.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from shop.models import EmailVerificationToken  # Убедитесь, что путь правильный
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, ChatMessage, Order, OrderItem
from .serializers import ChatRoomSerializer, ChatMessageSerializer, OrderSerializer, OrderItemSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        # Get the refresh token from the request
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        try:
            # Get user's cart
            cart = get_or_create_cart(request.user)
            cart_items = CartItems.objects.filter(cart=cart)
            
            if not cart_items.exists():
                return Response(
                    {"error": "Cart is empty"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate total price with Decimal for precision
            total_price = Decimal('0.0')
            for item in cart_items:
                item_price = Decimal(str(item.product.price))
                total_price += item_price * item.quantity
            
            # Ensure total_price is not zero
            if total_price <= 0:
                return Response(
                    {"error": "Invalid total price"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create order data with explicit total_price
            order_data = {
                'full_name': request.data.get('full_name'),
                'email': request.data.get('email'),
                'phone': request.data.get('phone'),
                'address': request.data.get('address'),
                'city': request.data.get('city'),
                'postal_code': request.data.get('postal_code'),
                'shipping_notes': request.data.get('shipping_notes'),
                'total_price': total_price  # Explicitly set total_price
            }
            
            # Validate the data
            serializer = self.get_serializer(data=order_data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save the order
            order = serializer.save(
                user=request.user,
                status='pending'
            )
            
            # Create order items
            order_items = []
            for item in cart_items:
                order_items.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                )
            
            # Bulk create order items
            if order_items:
                OrderItem.objects.bulk_create(order_items)
            
            # Clear cart items
            cart_items.delete()
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": f"Failed to create order: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Устанавливаем пользователя при создании комнаты
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = ChatMessage.objects.filter(room=room)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        try:
            room = self.get_object()
            message_text = request.data.get('message')
            
            if not message_text:
                return Response(
                    {"error": "Message text is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            message = ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=message_text
            )
            
            serializer = ChatMessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        room = self.get_object()
        unread_messages = ChatMessage.objects.filter(
            room=room,
            is_read=False
        ).exclude(sender=request.user)
        
        unread_messages.update(is_read=True)
        return Response({'status': 'messages marked as read'})


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserRegistrationForm(data)
            
            if form.is_valid():
                # Create user but set as inactive
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                # Generate verification token
                token = get_random_string(64)
                expires_at = timezone.now() + timedelta(hours=24)
                
                EmailVerificationToken.objects.create(
                    user=user,
                    token=token,
                    expires_at=expires_at
                )

                # Send verification email
                verification_url = f"http://localhost:3000/verify-email/{token}"
                context = {
                    'user': user,
                    'verification_url': verification_url
                }
                
                html_message = render_to_string('email/verification.html', context)
                
                send_mail(
                    subject='Verify your email address',
                    message='Please verify your email address',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message
                )

                return JsonResponse({
                    "status": "success",
                    "message": "Registration successful! Please check your email to verify your account.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "full_name": user.get_full_name(),
                    }
                }, status=201)
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid form data.",
                    "errors": form.errors
                }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": "Request processing failed.",
                "details": str(e)
            }, status=400)

    return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    try:
        verification = EmailVerificationToken.objects.get(token=token)
        
        if not verification.is_valid():
            return JsonResponse({
                "status": "error",
                "message": "Verification link has expired."
            }, status=400)

        user = verification.user
        user.is_active = True
        user.save()

        # Generate tokens for auto-login
        refresh = RefreshToken.for_user(user)

        verification.delete()

        return JsonResponse({
            "status": "success",
            "message": "Email verified successfully!",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        })
    except EmailVerificationToken.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Invalid verification token."
        }, status=400)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return super().get_permissions()

class CartItemsViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_or_create_cart(self.request.user)
        return CartItems.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = get_or_create_cart(self.request.user)
        serializer.save(cart=cart)

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] 
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            products = self.queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )[:5]  # Limit to 5 suggestions
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response([])

class FavouriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "status": "success",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=200)
        else:
            return JsonResponse({
                "status": "error",
                "message": "Invalid credentials."
            }, status=401)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "Request processing failed.",
            "details": str(e)
        }, status=400)