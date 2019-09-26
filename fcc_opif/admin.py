import csv
from django.contrib import admin
from django.http import HttpResponse
from fcc_opif.models import Facility, FacilityFolder, FacilityFile


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
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        '''all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.pyparameter_name
        )'''
        yield all_choice


class FacilityStateFilter(InputFilter):
    parameter_name = 'community_state'
    title = ('State')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                community_state=uid
            )


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


class FolderFacilityFilter(InputFilter):
    parameter_name = 'entity'
    title = ('Facility')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                entity=uid
            )


class FolderParentFilter(InputFilter):
    parameter_name = 'parent_folder'
    title = ('Parent Folder')

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                parent_folder__folder_path=uid
            )


'''
class GenericFilter(InputFilter):

    def __init__(self, parameter_name, title):
        self.parameter_name = parameter_name
        self.title = title

    parameter_name = 'l'
    title = 'l'

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()
            return queryset.filter(
                Q(uid)
            )
'''


class FacilityAdmin(admin.ModelAdmin):

    list_filter = ('service_type', FacilityStateFilter, FacilityCityFilter)
    search_fields = ['call_sign']
    list_display = (
        'call_sign',
        'service_type',
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

    list_filter = ('entity__call_sign', FolderParentFilter)
    search_fields = ['folder_path', 'entity_folder_id']
    list_display = (
        'entity', 
        'folder_path',
        'entity_folder_id',
        'file_count',
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


class FileAdmin(admin.ModelAdmin, ExportCsvMixin):

    list_filter = ('folder__entity__call_sign',)
    search_fields = [
        'file_name', 'folder__entity_folder_id', 'folder__folder_path'
    ]
    list_display = (
        'folder__entity',
        'file_name',
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
    list_select_related = ('folder__entity', )

    def folder__entity(self, obj):
        return obj.folder.entity
    
    folder__entity.short_description = 'Facility'
    folder__entity.admin_order_field = 'folder__entity'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(FacilityFile, FileAdmin)
