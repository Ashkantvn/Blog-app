from django.contrib import admin
from django.urls import path
from django.conf import settings
from core.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main pages
    path("", Home.as_view(), name="home"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)