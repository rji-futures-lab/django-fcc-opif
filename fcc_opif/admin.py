import csv
from django.contrib import admin
from django.http import HttpResponse
from fcc_opif.models import Facility, FacilityFolder, FacilityFile, CableSystem, CableCommunity, CableFolder, CableFile


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        model_name = self.model._meta
        field_names = self.list_display

        response = HttpResponse(content_type='text/csv')
        content_disposition = f'attachment; filename={model_name}.csv'
        response['Content-Disposition'] = content_disposition
        writer = csv.writer(response)

        writer.writerow(field_names)

        for obj in queryset:
            row = []
            for field in field_names:
                if '__' in field:
                    parts = field.split('__')
                    row.append(getattr(getattr(obj, parts[0]), parts[1]))
                elif callable(getattr(obj, field)):
                    row.append(getattr(obj, field)())
                else:
                    row.append(getattr(obj, field))
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected"


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        yield all_choice


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class FacilityCityFilter(InputFilter):
    parameter_name = 'community_city'
    title = ('City')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                community_city=uid
            )


class FolderPathFilter(InputFilter):
    parameter_name = 'folder_path'
    title = ('Folder Path')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                folder_path=uid
            )

class FileFolderFilter(InputFilter):
    parameter_name = 'folder_path'
    title = ('Folder Path')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                folder__folder_path=uid
            )

class FolderFacilityFilter(InputFilter):
    parameter_name = 'entity'
    title = ('Facility')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                entity=uid
            )


class FacilityFolderParentFilter(InputFilter):
    parameter_name = 'parent_folder'
    title = ('Parent Folder')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                parent_folder__folder_path=uid
            )

class CommunityCableSystemFilter(InputFilter):
    parameter_name = 'system'
    title = ('Cable System')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                system__legal_name=uid
            )

class FolderEntityFilter(InputFilter):
    parameter_name = 'folder__entity'
    title = ('Entity')
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                folder__entity__call_sign__icontains=uid
            )

class FacilityAdmin(admin.ModelAdmin):

    list_filter = (
        ('service_type', custom_titled_filter('Service Type')), 
        FacilityCityFilter, 
        ('has_missing_files', custom_titled_filter('Has Missing Files'))
    )
    search_fields = ['call_sign']
    list_display = (
        'call_sign',
        'service_type',
        'has_missing_files',
        '_actual_file_count',
        'expected_file_count',
        'community_city',
        'community_state',
        'facility_type',
        'party_name',
        'party_city',
        'party_state',
        'network_afil',
    )
    readonly_fields = (
        'id',
        'call_sign',
        'service',
        'service_type',
        '_actual_file_count',
        'expected_file_count',
        'rf_channel',
        'virtual_channel',
        'license_expiration_date',
        'status_date',
        'status',
        'community_city',
        'community_state',
        'facility_type',
        'frequency',
        'active_ind',
        'scanned_letter_ids',
        'party_name',
        'party_address1',
        'party_address2',
        'party_city',
        'party_zip1',
        'party_zip2',
        'party_state',
        'party_phone',
        'nielsen_dma',
        'network_afil',
        'band',
        'auth_app_id',
        'post_card_id',
    )
    ordering = ('service_type', 'call_sign',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Facility, FacilityAdmin)

class FolderAdmin(admin.ModelAdmin):

    list_filter = (FacilityFolderParentFilter,)
    search_fields = ['folder_path', 'entity_folder_id',]
    list_display = (
        'entity', 
        'folder_path',
        'entity_folder_id',
        'file_count',
        'actual_file_count',
        'create_ts',
        'last_update_ts',
    )
    list_display_links = ('folder_path',)
    readonly_fields = (
        'entity_folder_id',
        'folder_name',
        'folder_path',
        'allow_rename_ind',
        'allow_subfolder_ind',
        'allow_upload_ind',
        'allow_delete_ind',
        'more_public_files_ind',
        'parent_folder',
        'file_count',
        'create_ts',
        'last_update_ts',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    ordering = ('entity', 'folder_path',)


admin.site.register(FacilityFolder, FolderAdmin)
admin.site.register(CableFolder, FolderAdmin)

class FileAdmin(admin.ModelAdmin, ExportCsvMixin):

    search_fields = (
        'file_name', 'folder__entity_folder_id', 'folder__folder_path',
    )
    
    list_filter = (FileFolderFilter, FolderEntityFilter, ('missing_stored_file', custom_titled_filter("Has File Stored")))
    list_display = (
        'folder__entity',
        'file_name',
        'missing_stored_file',
        'folder',
        'file_id',
        'file_extension',
        'file_size',
        'file_status',
        'create_ts',
        'last_update_ts',
        'file_manager_id',
        'moved_from',
        'moved_ts',
        'url',
        'documentcloud_id',
    )
    list_display_links = ('file_name',)
    readonly_fields = (
        'file_id',
        'file_name',
        'file_extension',
        'file_size',
        'file_status',
        'create_ts',
        'last_update_ts',
        'file_manager_id',
        'moved_from',
        'moved_ts',
        'documentcloud_id',
        'stored_file',
    )
    actions = ["export_as_csv"]
    ordering = ('folder__entity', 'folder', 'file_name')
    list_select_related = ('folder__entity',)

    def folder__entity(self, obj):
        return obj.folder.entity

    folder__entity.short_description = 'Entity'
    folder__entity.admin_order_field = 'folder__entity'
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(FacilityFile, FileAdmin)
admin.site.register(CableFile, FileAdmin)

class CableSystemAdmin(admin.ModelAdmin):

    search_fields = ('legal_name', 'id',)
    list_filter = (('has_missing_files', custom_titled_filter('Has Missing Files')),)
    list_display = (
        'id',
        'legal_name',
        'has_missing_files',
        '_actual_file_count',
        'expected_file_count',
    )
    readonly_fields = (
        "id",
        "legal_name",
        "service_type",
        "_actual_file_count",
        'expected_file_count',
        "operator_address_line1",
        "operator_name",
        "operator_address_line2",
        "operator_po_box",
        "operator_city",
        "operator_zipcode",
        "operator_zipcode_suffix",
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
        "principal_zipcode",
        "principal_zipcode_suffix",
        "principal_fax",
        "principal_phone",
        "principal_email",
        "local_file_contact_name",
        "local_file_address_line1",
        "local_file_address_line2",
        "local_file_po_box",
        "local_file_city",
        "local_file_state",
        "local_file_zipcode",
        "local_file_zipcode_suffix",
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

admin.site.register(CableSystem, CableSystemAdmin)

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

admin.site.register(CableCommunity, CableCommunityAdmin)