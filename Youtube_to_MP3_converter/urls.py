from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from core.sitemap import StaticViewSitemap

sitemaps = {
    'static':StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('sitemap.xml',sitemap,{'sitemaps': sitemaps})
]
