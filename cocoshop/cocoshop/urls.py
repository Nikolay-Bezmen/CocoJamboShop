# myproject/urls.py
import django_private_chat2.views
from django.contrib import admin
from django.urls import include, path, re_path
from shop.views import ProductViewSet, UserViewSet, ProtectedView, CartItemsViewSet, FavouriteViewSet
from shop.services import cartoperations, liked
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'cart-items', CartItemsViewSet, basename='cart')
router.register(r'favourites', FavouriteViewSet, basename='favourites')


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API for your project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('api/', include(router.urls), ),
                  path('admin/', admin.site.urls),
                  path("api/add-to-favourites/<int:prid>", liked.add_to_favourites, name="AddToFavourite"),
                  path("api/remove-from-favourites/<int:prid>", liked.remove_from_favourites, name="RemoveFromFavourite"),
                  path("api/check-favourites/<int:prid>", liked.check_favourites, name="CheckFavourites"),
                  path("api/add-to-cart/<int:prid>", cartoperations.add_to_cart, name="AddToCart"),
                  path("api/check-cart/<int:prid>", cartoperations.check_cart, name="CheckCartProduct"),
                  path("api/delete-from-cart/<int:prid>", cartoperations.delete_from_cart, name="DeleteFromCart"),
                  path("api/delete-all-from-cart/<int:prid>", cartoperations.delete_all_from_cart, name="DeleteAllFromCart"),
                  path("api/clear-cart/", cartoperations.clear_cart, name="ClearCart"),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/protected/', ProtectedView.as_view(), name='protected_view'),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('shop/', include('shop.urls')),
                  re_path(r'', include('django_private_chat2.urls', namespace='django_private_chat2')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
