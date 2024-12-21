

# shop/urls.py

from django.urls import path


from shop.views import UserViewSet, ProductViewSet, user_register, user_login
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
]

