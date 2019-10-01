from django.db import models
from django.contrib.postgres.fields import JSONField
import requests
from fcc_opif.constants import FCC_API_URL
from fcc_opif.utils import camelcase_to_underscore, json_cleaner
from .base import FileBase, FolderBase, MissingFileManager
from fcc_opif.handlers import refresh_folder


class CableCommunity(models.Model):
    community_unit_id = models.CharField(max_length=200, primary_key=True)
    system = models.ForeignKey(
        'CableSystem',
        related_name='communities',
        on_delete=models.CASCADE
    )
    community_name = models.CharField(max_length=200)
    county_name = models.CharField(max_length=200)

    def __str__(self):
        return self.community_name

    class Meta:
        verbose_name = 'Cable Community'
        verbose_name_plural = 'Cable Communities'


class CableFile(FileBase):
    folder = models.ForeignKey(
        'CableFolder',
        related_name='files',
        on_delete=models.CASCADE,
        db_column='folder_id',
        editable=False,
    )
    #missing_files = MissingFileManager()


class CableFolder(FolderBase):
    entity = models.ForeignKey(
        'CableSystem',
        related_name='folders',
        on_delete=models.CASCADE,
        db_column='entity_id',
        editable=False,
    )


class CableSystem(models.Model):
    id = models.CharField(max_length=200, primary_key=True, editable=False)
    legal_name = models.CharField(max_length=200, editable=False)
    service_type = models.CharField(max_length=200, editable=False)
    operator_address_line1 = models.CharField(max_length=200, editable=False)
    operator_name = models.CharField(max_length=200, editable=False)
    operator_address_line2 = models.CharField(max_length=200, editable=False)
    operator_po_box = models.CharField(max_length=200, editable=False)
    operator_city = models.CharField(max_length=200, editable=False)
    operator_zipcode = models.CharField(max_length=200, editable=False)
    operator_zipcode_suffix = models.CharField(max_length=200, editable=False)
    operator_state = models.CharField(max_length=2, editable=False)
    operator_email = models.CharField(max_length=200, blank=True, editable=False)
    operator_website = models.CharField(max_length=200, blank=True, editable=False)
    operator_phone = models.CharField(max_length=200, blank=True, editable=False)
    operator_fax = models.CharField(max_length=200, blank=True, editable=False)

    cores_user = models.CharField(max_length=200, editable=False)

    principal_headend_name = models.CharField(max_length=200, blank=True, editable=False)
    principal_address_line1 = models.CharField(max_length=200, blank=True, editable=False)
    principal_address_line2 = models.CharField(max_length=200, blank=True, editable=False)
    principal_po_box = models.CharField(max_length=200, blank=True, editable=False)
    principal_city = models.CharField(max_length=200, blank=True, editable=False)
    principal_state = models.CharField(max_length=200, blank=True, editable=False)
    principal_zipcode = models.CharField(max_length=200, blank=True, editable=False)
    principal_zipcode_suffix = models.CharField(max_length=200, blank=True, editable=False)
    principal_fax = models.CharField(max_length=200, blank=True, editable=False)
    principal_phone = models.CharField(max_length=200, blank=True, editable=False)
    principal_email = models.CharField(max_length=200, blank=True, editable=False)

    local_file_contact_name = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_address_line1 = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_address_line2 = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_po_box = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_city = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_state = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_zipcode = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_zipcode_suffix = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_contact_fax = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_contact_phone = models.CharField(
        max_length=200, blank=True, editable=False
    )
    local_file_contact_email = models.CharField(
        max_length=200, blank=True, editable=False
    )

    active_ind = models.BooleanField(null=True)
    principal_address_in_local_files = models.BooleanField(null=True)
    cable_service_zip_codes = JSONField(null=True)
    cable_service_emp_units = JSONField(null=True)
    cable_communities = JSONField(null=True)
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

        psid = self.id
        endpoint_url = f"{FCC_API_URL}/service/cable/psid/{psid}.json"

        r = requests.get(endpoint_url)

        for key, value in r.json()['results']['cableSystemInfo'].items():
            if key == 'cableServiceZipCodes' or key == 'cableServiceEmpUnits' or key == 'cableCommunities':
                pass
            elif type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False
            setattr(self, camelcase_to_underscore(key), value)
        
        for item in r.json()['results']['cableSystemInfo']['cableServiceZipCodes'].items():
            if key == 'zipcodes':
                setattr(self, camelcase_to_underscore(key), value)

        for item in r.json()['results']['cableSystemInfo']['cableServiceEmpUnits'].items():
            if key == 'empUnits':
                setattr(self, camelcase_to_underscore(key), value)
        
        for community in r.json()['results']['cableSystemInfo']['cableCommunities']:
            clean_community_data = json_cleaner(community)
            community, created = self.communities.update_or_create(
                defaults=clean_community_data,
                community_unit_id=clean_community_data["community_unit_id"]
            )

        return self.save()

    def refresh_all_files(self):
        
        self.actual_file_count = 0
        self.expected_file_count = 0

        entityID = self.id
        endpoint_url = f"{FCC_API_URL}/manager/folder/parentFolders.json?entityId={entityID}&sourceService=cable"  # noqa

        r = requests.get(endpoint_url)

        r.raise_for_status()

        folder_list = r.json()['folders']
        for folder_data in folder_list:
            clean_data = json_cleaner(folder_data)
            clean_data['entity_id'] = self.id
            folder, created = self.folders.update_or_create(defaults = clean_data, entity_folder_id = clean_data["entity_folder_id"])  # noqa
            refresh_folder('CableFolder', folder.entity_folder_id)
            print(folder._actual_file_count)

            self.actual_file_count += folder._actual_file_count
            self.expected_file_count += int(folder.file_count)
            if self.actual_file_count == self.expected_file_count:
                setattr(self, 'has_missing_files', False)
            else:
                setattr(self, 'has_missing_files', True)

            self.save()

        return self.save()

    def __str__(self):
        return self.legal_name

    class Meta:
        verbose_name = 'Cable System'
        verbose_name_plural = "Cable Systems"