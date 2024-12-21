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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Разрешаем просмотр продуктов всем
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

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