"""
URL configuration for blog_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
from django.conf import settings
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve,{'document_root' : settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve,{'document_root' : settings.STATIC_ROOT}),
]


urlpatterns += i18n_patterns(
    path(_(r'admin/'), admin.site.urls),
    path(_(r""), views.home_view),
    path(_(r"about/"), views.about_view),
    path(_(r"posts/"), include("posts.urls")),
    path(_(r"users/"), include("users.urls"))
)
