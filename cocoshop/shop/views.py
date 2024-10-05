# shop/views.py

from rest_framework import generics
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User  # Используйте вашу модель

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()  # Замените на вашу модель
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # Замените на вашу модель
    serializer_class = UserSerializer

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Используйте метод save() формы
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Перенаправление на страницу логина после успешной регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
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
