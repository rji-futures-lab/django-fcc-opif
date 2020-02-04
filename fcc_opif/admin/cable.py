from django.contrib import admin
from django.http import HttpResponse
from fcc_opif.admin.filters import (
    CommunityCableSystemFilter
)
from fcc_opif.models import (
    CableSystem, CableCommunity, CableFolder, CableFile
)


@admin.register(CableSystem)
class CableSystemAdmin(admin.ModelAdmin):

    search_fields = ('legal_name', 'id',)
    list_display = (
        'id',
        'legal_name',
    )
    readonly_fields = (
        "id",
        "legal_name",
        "service_type",
        "operator_address_line1",
        "operator_name",
        "operator_address_line2",
        "operator_po_box",
        "operator_city",
        "operator_zip_code",
        "operator_zip_code_suffix",
        "operator_state",
        "operator_email",
        "operator_website",
        "operator_phone",
        "operator_fax",
        "cores_user",
        "principal_headend_name",
        "principal_address_line1",
        "principal_address_line2",
        "principal_po_box",
        "principal_city",
        "principal_state",
        "principal_zip_code",
        "principal_zip_code_suffix",
        "principal_fax",
        "principal_phone",
        "principal_email",
        "local_file_contact_name",
        "local_file_address_line1",
        "local_file_address_line2",
        "local_file_po_box",
        "local_file_city",
        "local_file_state",
        "local_file_zip_code",
        "local_file_zip_code_suffix",
        "local_file_contact_fax",
        "local_file_contact_phone",
        "local_file_contact_email",
        "active_ind",
        "principal_address_in_local_files",
        "cable_service_zip_codes",
        "cable_service_emp_units",
        "cable_communities",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CableCommunity)
class CableCommunityAdmin(admin.ModelAdmin):

    list_filter = (CommunityCableSystemFilter, 'system__legal_name')
    search_fields = ['community_name']
    readonly_fields = (
        "community_unit_id",
        "system",
        "community_name",
        "county_name",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
