# shop/urls.py

from django.urls import path


from shop.views.views import UserViewSet, ProductViewSet, user_register, user_login, home, \
    shopping_cart, \
    page_not_found, liked, contacts, add_to_cart
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', user_login, name='login'),
    path('liked/', liked, name='liked'),
    path('home/', home, name='home'),
    path('home/shoppingCart', shopping_cart, name='cart'),
    path('register/', user_register, name='register'),
    path('contacts/', contacts, name='contacts'),
    path('products/add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]

handler404 = page_not_found

