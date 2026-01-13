from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path,include
from .views import api_route_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_route_view),
    path('api/', include('api.urls') , name='api-root'),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)