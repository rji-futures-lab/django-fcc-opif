import csv
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils.html import format_html
from fcc_opif.admin.filters import (
    EntityFilter,
    FileFolderPathFilter,
    FolderEntityFilter,
    FolderPathFilter,
    HasStoredFile,
)
from fcc_opif.models import (
    FacilityFolder, FacilityFile,
    CableFolder, CableFile,
    FacilityFilePage, CableFilePage,
)


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


@admin.register(CableFile, FacilityFile)
class FileAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_per_page = 25
    date_hierarchy = 'last_update_ts'
    search_fields = (
        'file_name', 'folder__entity_folder_id', 'folder__folder_path',
    )
    list_filter = (
        FileFolderPathFilter,
        FolderEntityFilter,
        HasStoredFile,
    )
    list_display = (
        'folder__entity',
        'file_name',
        'display_url',
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
        'has_stored_file',
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

    '''
    def change_view(self, request, object_id, form_url="", extra_context=None):
        pass
    '''

    def display_url(self, obj):
        return format_html(f"<a href='{reverse('extractor', args=[obj.file_id])}'>Extractor</a>")
        #return format_html("<a href='/fcc_opif/extractor/{id}'>Extractor</a>", id=obj.file_id)

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

    def has_stored_file(self, obj):
        if obj.stored_file:
            html = format_html(
                '<img src="/static/admin/img/icon-yes.svg" alt="True">'
            )
        else:
            html = format_html(
                '<img src="/static/admin/img/icon-no.svg" alt="False">'
            )
        return html


# @admin.register(CableFilePage, FacilityFilePage)
# class FilePageAdmin(admin.ModelAdmin):
#     list_per_page = 25
#     list_display = (
#         'image', 
#         'file',
#         'page_num',
#     )
#     readonly_fields = (
#         'image', 
#         'file',
#         'page_num',
#     )

#     def has_add_permission(self, request, obj=None):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False


@admin.register(CableFolder, FacilityFolder)
class FolderAdmin(admin.ModelAdmin):
    list_per_page = 25
    date_hierarchy = 'last_update_ts'
    list_filter = (FolderPathFilter, EntityFilter)
    search_fields = ['folder_path', 'entity_folder_id',]
    list_display = (
        'entity', 
        'folder_path',
        'entity_folder_id',
        'file_count',
        'create_ts',
        'last_update_ts',
        'more_public_files_ind',
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
    ordering = ('entity', 'folder_path',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
