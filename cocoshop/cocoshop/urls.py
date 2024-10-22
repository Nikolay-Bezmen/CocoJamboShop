# myproject/urls.py

from django.contrib import admin
from django.urls import include, path
from shop.views.views import ProductViewSet, UserViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
                  path('api/', include(router.urls),),
                  path('admin/', admin.site.urls),
                  path('shop/', include('shop.urls'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)