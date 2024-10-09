# shop/urls.py

from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, user_register, user_login, home, shopping_cart

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('home/shoppingCart', shopping_cart, name='cart'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('register/', user_register, name='register'),
]
