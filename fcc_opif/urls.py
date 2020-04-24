from django.contrib import admin
from fcc_opif import views
from django.urls import path

urlpatterns = [
    path('facility_extractor/<file_id>', views.facilityfile, name='facility_extractor'),
    path('cable_system_extractor/<file_id>', views.cablesystemfile, name='cable_system_extractor'),
]
