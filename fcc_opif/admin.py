import csv
from django.contrib import admin
from django.http import HttpResponse
from fcc_opif.models import Facility, FacilityFolder, FacilityFile

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        model_name = self.model._meta
        field_names = self.list_display

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={model_name}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

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

admin.site.register(Facility, FacilityAdmin)

class FolderAdmin(admin.ModelAdmin):

    list_filter = ('entity__call_sign', FolderParentFilter)
    search_fields = ['folder_path', 'entity_folder_id']

admin.site.register(FacilityFolder, FolderAdmin)

class FileAdmin(admin.ModelAdmin, ExportCsvMixin):

    list_filter = ('file_name',)
    search_fields = ['file_name', 'folder__entity_folder_id', 'folder__folder_path']
    list_display = (
        'file_id',
        'folder',
        'file_name',
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
    actions = ["export_as_csv"]


admin.site.register(FacilityFile, FileAdmin)


