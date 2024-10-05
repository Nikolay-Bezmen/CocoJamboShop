# shop/urls.py

from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, register, login  # Добавьте импорт register

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', login, name='login'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('register/', register, name='register'),
]
