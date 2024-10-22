# shop/urls.py

from django.urls import path

from shop.views.product_views import ProductCreateView, ProductDeleteView, ProductUpdateView, ProductDetailView, \
    ProductListView
from shop.views.users_views import UserCreateView, UserDeleteView, UserUpdateView, UserListView, UserDetailView
from shop.views.views import UserViewSet, ProductViewSet, user_register, user_login, home, \
    shopping_cart, \
    page_not_found, liked, contacts, add_to_cart
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', user_login, name='login'),
    path('liked/', liked, name='liked'),

    path('home/', home, name='home'),
    path('home/shoppingCart', shopping_cart, name='cart'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('register/', user_register, name='register'),
    # path('products/', ProductListView.as_view(), name='product_list'),
    path('contacts/', contacts, name='contacts'),
    path('products/add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('products/new/', ProductCreateView.as_view(), name='product_create'),

    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),


    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/new/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

]

handler404 = page_not_found

