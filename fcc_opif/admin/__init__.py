from django.contrib import admin
from django.urls import path
from fcc_opif.views import facilityfile

from fcc_opif.admin.cable import(
    CableCommunityAdmin,
    CableSystemAdmin,
)
from fcc_opif.admin.facilities import (
    FacilityAdmin
)
from fcc_opif.admin.files import(
    FileAdmin,
    FolderAdmin,
)

from fcc_opif.admin.file_forms import FileFormAdmin

__all__ = (
    'CableCommunityAdmin',
    'CableSystemAdmin',
    'FileAdmin',
    'FolderAdmin',
    'FileFormAdmin',
)