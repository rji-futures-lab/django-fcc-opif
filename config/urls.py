"""
Django project URL configuration.

The `urlpatterns` list routes URLs to views.

For more information, check out
https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from fcc_opif import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fcc_opif/', include('fcc_opif.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
