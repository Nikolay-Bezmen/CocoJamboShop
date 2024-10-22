# shop/views.py

from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound
from rest_framework import generics
from shop.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.forms import UserRegistrationForm
from shop.services.services import ProductService, CartServices, CartListService
from shop.models import User, Products, Categories, CartItems, Carts
from shop.serializers import ProductSerializer, UserSerializer, OrderSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductService.get_all_products()
    serializer_class = ProductSerializer


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Неверные имя пользователя или пароль."
            return render(request, 'login/login.html', {'error_message': error_message})

    return render(request, 'login/login.html')


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
