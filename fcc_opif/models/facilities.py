from django.contrib.postgres.fields import JSONField
from django.db import models
import requests
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.handlers import refresh_folder
from fcc_opif.utils import camelcase_to_underscore, json_cleaner
from .base import FileBase, FolderBase, MissingFileManager


class Facility(models.Model):
    id = models.CharField(editable=False, max_length=200, primary_key=True)

    call_sign = models.CharField(editable=False, max_length=200)
    service = models.CharField(editable=False, max_length=200)
    service_type = models.CharField(
        editable=False, max_length=2, choices=SERVICE_TYPES
    )
    rf_channel = models.IntegerField(editable=False, null=True)
    virtual_channel = models.IntegerField(editable=False, null=True)
    license_expiration_date = models.CharField(editable=False, max_length=10)
    status_date = models.CharField(editable=False, max_length=10)
    status = models.CharField(editable=False, max_length=200)
    community_city = models.CharField(editable=False, max_length=200)
    community_state = models.CharField(
        editable=False, max_length=2
    )  # all states abbreviated?
    facility_type = models.CharField(editable=False, max_length=200)
    frequency = models.DecimalField(
        editable=False, max_digits=5, decimal_places=1
    )
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
    cc_contact = JSONField(editable=False, blank=True, null=True)
    _actual_file_count = models.IntegerField(editable=False, null=True, db_column="actual_file_count")
    _expected_file_count = models.IntegerField(editable=False, null=True, db_column="expected_file_count")
    has_missing_files = models.BooleanField(default=False)

    @property
    def actual_file_count(self):
        return self._actual_file_count

    @actual_file_count.setter
    def actual_file_count(self, value):
        self._actual_file_count = value

    @property
    def expected_file_count(self):
        return self._expected_file_count

    @expected_file_count.setter
    def expected_file_count(self, value):
        self._expected_file_count = value

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
                elif 'channel' in key.lower() and value == '':
                    value = None
            setattr(self, camelcase_to_underscore(key), value)

        return self.save()

    def refresh_all_files(self):
        """
        Call FCC's API to get details for the facility.

        Create new folders and files, update existing ones.
        """
        self.actual_file_count = 0
        self.expected_file_count = 0

        serviceType = self.service_type
        entityID = self.id
        endpoint_url = f"{FCC_API_URL}/manager/folder/parentFolders.json?entityId={entityID}&sourceService={serviceType}"  # noqa

        r = requests.get(endpoint_url)

        r.raise_for_status()

        folder_list = r.json()['folders']
        for folder_data in folder_list:
            clean_data = json_cleaner(folder_data)
            clean_data['entity_id'] = self.id
            folder, created = self.folders.update_or_create(
                defaults=clean_data,
                entity_folder_id=clean_data["entity_folder_id"],
            )
            refresh_folder('FacilityFolder', folder.entity_folder_id)
            
            print(folder._actual_file_count)
            print(int(folder.file_count))

            self.actual_file_count += folder.actual_file_count
            self.expected_file_count += int(folder.file_count)

            if self.actual_file_count == self.expected_file_count:
                setattr(self, 'has_missing_files', False)
            else:
                setattr(self, 'has_missing_files', True)

            self.save()

        return self.save()

    def __str__(self):
        return self.call_sign

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = "Facilities"
        indexes = [
            models.Index(fields=['service_type', 'call_sign']),
        ]


class FacilityFile(FileBase):
    folder = models.ForeignKey(
        'FacilityFolder',
        related_name='files',
        on_delete=models.CASCADE,
        db_column='folder_id',
        editable=False,
    )
    #missing_files = MissingFileManager()


class FacilityFolder(FolderBase):
    entity = models.ForeignKey(
        'Facility',
        related_name='folders',
        on_delete=models.CASCADE,
        db_column='entity_id',
        editable=False,
    )
