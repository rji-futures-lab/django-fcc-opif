"""
Django project URL configuration.

The `urlpatterns` list routes URLs to views.

For more information, check out
https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from fcc_opif import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fcc_opif/', include('fcc_opif.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    ) + urlpatterns
