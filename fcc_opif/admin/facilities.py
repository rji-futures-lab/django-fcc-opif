from django.contrib import admin
from django.http import HttpResponse
from fcc_opif.admin.filters import (
    FacilityCityFilter,
    FacilityStateFilter,
    FacilityPartyNameFilter,
    FacilityNetworkAffiliateFilter,
)
from fcc_opif.models import Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_per_page = 25
    date_hierarchy = 'last_refreshed_ts'
    list_filter = (
        'service_type', 
        FacilityCityFilter,
        FacilityStateFilter,
        FacilityPartyNameFilter,
        FacilityNetworkAffiliateFilter,
    )
    search_fields = ['call_sign', 'id']
    list_display = (
        'call_sign',
        'id',
        'service_type',
        'community_city',
        'community_state',
        'facility_type',
        'party_name',
        'party_city',
        'party_state',
        'network_afil',
        'last_refreshed_ts'
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
        'last_refreshed_ts'
    )
    ordering = ('service_type', 'call_sign',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
