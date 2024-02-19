"""
URL configuration for artistic_edge project.

"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('basket/', include('store_basket.urls', namespace='store_basket')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('store.urls', namespace='store')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    