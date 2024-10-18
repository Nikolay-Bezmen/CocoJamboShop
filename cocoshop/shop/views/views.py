# shop/views.py

from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound
from rest_framework import generics
from shop.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.forms import UserRegistrationForm
from shop.models import User, Products, Categories, CartItems, Carts
from shop.serializers import ProductSerializer, UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Перенаправление на страницу логина после успешной регистрации
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
            return redirect('home')  # Перенаправление на главную страницу после входа
        else:
            # Вывод сообщения об ошибке
            error_message = "Неверные имя пользователя или пароль."
            return render(request, 'login/login.html', {'error_message': error_message})

    return render(request, 'login/login.html')


def home(request):
    return render(request, 'main/index.html')


def liked(request):
    return render(request, 'main/liked.html', )


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
