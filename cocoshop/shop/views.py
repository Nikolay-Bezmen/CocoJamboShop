# shop/views.py

from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound
from rest_framework import generics
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from shop.forms import UserRegistrationForm
from shop.services.services import ProductService, CartServices, CartListService
from shop.models import User, Products, Categories, CartItems, Carts, Favourite
from shop.serializers import UserSerializer, OrderSerializer, CartItemsSerializer, ProductSerializer, \
    FavouriteSerializer
from shop.services.cartoperations import get_or_create_cart
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CartItemsViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_or_create_cart(self.request.user)
        return CartItems.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = get_or_create_cart(self.request.user)
        serializer.save(cart=cart)


class FavouriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return all favourite items for the authenticated user
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the favourite item with the current user
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "This is a protected view!"})


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            form = UserRegistrationForm(data)

            if form.is_valid():
                # Save the user without immediately committing to the database
                user = form.save(commit=True)
                user.save()  # Commit to the database

                return JsonResponse({
                    "status": "success",
                    "message": "Your account has been created successfully!",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "full_name": user.get_full_name(),
                    }
                }, status=201)
            else:
                # Collect form errors
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


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Читаем тело запроса
            username = data.get("username")
            password = data.get("password")

            # Аутентификация пользователя
            user = authenticate(request, username=username, password=password)
            print("-------------------------------------------------------------------")
            if user is not None:
                login(request, user)

                # Создание токенов
                refresh = RefreshToken.for_user(user)
                token_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return JsonResponse({"status": "success", "tokens": token_data}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Неверные имя пользователя или пароль."}, status=401)
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Ошибка обработки запроса.", "details": str(e)},
                                status=400)
    return JsonResponse({"status": "error", "message": "Метод не поддерживается."}, status=405)


def page_not_found(request, exception):
    return HttpResponseNotFound("Page not found")


