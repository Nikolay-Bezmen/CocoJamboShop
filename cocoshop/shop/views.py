# shop/views.py

from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound
from rest_framework import generics
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from shop.forms import UserRegistrationForm
from shop.services.services import ProductService, CartServices, CartListService
from shop.models import User, Products, Categories, CartItems, Carts
from shop.serializers import UserSerializer, OrderSerializer, CartItemsSerializer, ProductSerializer
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
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)  # Сохраняем объект без записи в базу данных
            print(user.id)
            print(user.get_full_name())
            user.save()  # Сохраняем объект и получаем его `id`
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


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


def home(request):
    return render(request, 'main/index.html')


def liked(request):
    return render(request, 'main/liked.html', )


def add_to_cart(request, product_id):
    user_cart = Carts.objects.get(user=request.user)
    user_items = CartItems.objects.create(cart=user_cart, product=product_id)
    user_items.quantity += 1


def shopping_cart(request):
    user_cart = Carts.objects.get(user=request.user)
    context = {
        'cartItems': CartItems.objects.filter(cart=user_cart),
    }
    return render(request, 'main/shoppingCart.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("Page not found")


def contacts(request):
    return "contacts"
