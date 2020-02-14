from django.contrib import admin
from fcc_opif import views
from django.urls import path

urlpatterns = [
    path('extractor/<uuid:file_id>', views.facilityfile, name='extractor'),
]
