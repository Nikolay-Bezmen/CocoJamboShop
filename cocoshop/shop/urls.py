# shop/urls.py

from django.urls import path


from shop.views import UserViewSet, ProductViewSet, user_register, user_login, page_not_found
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
]

handler404 = page_not_found

