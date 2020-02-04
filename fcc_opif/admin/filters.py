from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )        
        yield all_choice


class HasStoredFile(admin.SimpleListFilter):
    title = _('Has stored file')
    parameter_name = 'has_stored_file'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no',  _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            queryset = queryset.filter(stored_file__isnull=False)
        elif self.value() == 'no':
            queryset = queryset.filter(
                Q(stored_file__isnull=True) | Q(stored_file__exact='')
            )
        return queryset


class FacilityCityFilter(InputFilter):
    parameter_name = 'community_city'
    title = ('City')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                community_city__iexact=self.value()
            )


class FacilityStateFilter(InputFilter):
    parameter_name = 'community_state'
    title = ('State')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                community_state__iexact=self.value()
            )


class FileFolderPathFilter(InputFilter):
    parameter_name = 'folder_path'
    title = ('Folder Path')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                folder__folder_path__icontains=self.value()
            )


class FolderPathFilter(InputFilter):
    parameter_name = 'folder_path'
    title = ('Folder Path')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                folder_path__icontains=self.value()
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
            if queryset.model._meta.model_name == 'CableFile':
                queryset = queryset.filter(
                    folder__entity__legal_name__icontains=self.value()
                )
            elif queryset.model._meta.model_name == 'FacilityFile':
                queryset = queryset.filter(
                    folder__entity__call_sign__icontains=self.value()
                )
            return queryset


class EntityFilter(InputFilter):
    parameter_name = 'entity'
    title = ('Entity')
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            if queryset.model._meta.model_name == 'CableFile':
                queryset = queryset.filter(
                    entity__legal_name__icontains=self.value()
                )
            elif queryset.model._meta.model_name == 'FacilityFile':
                queryset = queryset.filter(
                    entity__call_sign__icontains=self.value()
                )
            return queryset