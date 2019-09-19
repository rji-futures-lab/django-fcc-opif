from django.contrib.postgres.fields import JSONField
from django.db import models
import requests
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.utils import camelcase_to_underscore, json_cleaner
from .base import FileBase, FolderBase


class Facility(models.Model):
    id = models.CharField(editable=False, max_length=200, primary_key=True)

    call_sign = models.CharField(editable=False, max_length=200)
    service = models.CharField(editable=False, max_length=200)
    service_type = models.CharField(
        editable=False, max_length=2, choices=SERVICE_TYPES
    )
    rf_channel = models.IntegerField(editable=False)
    virtual_channel = models.IntegerField(editable=False)
    license_expiration_date = models.CharField(editable=False, max_length=10)
    status_date = models.CharField(editable=False, max_length=10)
    status = models.CharField(editable=False, max_length=200)
    community_city = models.CharField(editable=False, max_length=200)
    community_state = models.CharField(
        editable=False, max_length=2
    )  # all states abbreviated?
    facility_type = models.CharField(editable=False, max_length=200)
    frequency = models.DecimalField(
        editable=False, max_digits=4, decimal_places=1
    )  # ??
    active_ind = models.BooleanField(editable=False, )
    scanned_letter_ids = models.CharField(
        editable=False, max_length=200, blank=True
    )
    party_name = models.CharField(editable=False, max_length=200)
    party_address1 = models.CharField(editable=False, max_length=200)
    party_address2 = models.CharField(editable=False, max_length=200)
    party_city = models.CharField(editable=False, max_length=200)
    party_zip1 = models.CharField(editable=False, max_length=5)
    party_zip2 = models.CharField(editable=False, max_length=5, blank=True)
    party_state = models.CharField(editable=False, max_length=2)
    party_phone = models.CharField(editable=False, max_length=13)
    nielsen_dma = models.CharField(editable=False, max_length=200)
    network_afil = models.CharField(editable=False, max_length=200)
    band = models.CharField(editable=False, max_length=200)
    auth_app_id = models.CharField(editable=False, max_length=7)
    post_card_id = models.CharField(editable=False, max_length=7)
    main_studio_contact = JSONField(editable=False)
    cc_contact = JSONField(editable=False)

    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the facility.
        """
        serviceType = self.service_type
        entityID = self.id
        endpoint_url = f"{FCC_API_URL}/service/{serviceType}/facility/id/{entityID}.json"  # noqa

        r = requests.get(endpoint_url)

        r.raise_for_status()

        for key, value in r.json()['results']['facility'].items():
            if type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False
            setattr(self, camelcase_to_underscore(key), value)

        return self.save()

    def refresh_all_files(self):
        """
        Call FCC's API to get details for the facility.

        Create new folders and files, update existing ones.
        """

        serviceType = self.service_type
        entityID = self.id
        endpoint_url = f"{FCC_API_URL}/manager/folder/parentFolders.json?entityId={entityID}&sourceService={serviceType}"  # noqa

        r = requests.get(endpoint_url)

        r.raise_for_status()

        folder_list = r.json()['folders']
        for folder_data in folder_list:
            clean_data = json_cleaner(folder_data)
            clean_data['entity_id'] = self.id
            folder, created = self.folders.update_or_create(defaults = clean_data, entity_folder_id = clean_data["entity_folder_id"])  # noqa
            folder.refresh_from_fcc()

        return self.save()

    def __str__(self):
        return self.call_sign

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = "Facilities"


class FacilityFile(FileBase):
    folder = models.ForeignKey(
        'FacilityFolder',
        related_name='files',
        on_delete=models.CASCADE,
        db_column='folder_id',
        editable=False,
    )


class FacilityFolder(FolderBase):
    entity = models.ForeignKey(
        'Facility',
        related_name='folders',
        on_delete=models.CASCADE,
        db_column='entity_id',
        editable=False,
    )
