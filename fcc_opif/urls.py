from django.contrib import admin
from fcc_opif import views
from django.urls import path

urlpatterns = [
    path('facility_extractor/<file_id>', views.facilityfile, name='facility_extractor'),
    path('cable_system_extractor/<file_id>', views.cablesystemfile, name='cable_system_extractor'),
    path('fileform_list', views.FileFormList.as_view(), name='file_form_list'),
    path('fileform_create', views.FileFormCreate.as_view(), name='file_form_create'),
    path('fileform_update', views.update_form, name='update_form'),
]
