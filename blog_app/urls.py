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
from . import views,sitemaps
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.contrib.sitemaps.views import sitemap


sitemaps={
    'static':sitemaps.StaticViewSiteMap,
    'posts':sitemaps.PostsViewSiteMap,
    'podcasts':sitemaps.PodcastsViewSiteMap
}


urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve,{'document_root' : settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve,{'document_root' : settings.STATIC_ROOT}),
    re_path(r'^robots\.txt', include('robots.urls')),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap",),
]


urlpatterns += i18n_patterns(
    path(_(r'admin/'), admin.site.urls),
    path(_(r""), views.home_view,name='home'),
    path(_(r"about/"), views.about_view,name='about'),
    path(_(r"setting"), views.change_lang_view,name='settings'),
    path(_(r"posts/"), include("posts.urls")),
    path(_(r"users/"), include("users.urls")),
    path(_(r"podcasts/"), include("podcasts.urls")),
)
