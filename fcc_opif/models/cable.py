from django.db import models
from django.contrib.postgres.fields import JSONField
import requests
from fcc_opif.constants import FCC_API_URL
from fcc_opif.utils import camelcase_to_underscore
from .base import FileBase, FolderBase


class CableCommunity(models.Model):
    community_unit_id = models.CharField(max_length=200, primary_key=True)
    channel = models.ForeignKey(
        'CableSystem',
        related_name='communities',
        on_delete=models.CASCADE
    )
    community_name = models.CharField(max_length=200)
    county_name = models.CharField(max_length=200)

    def __str__(self):
        return self.community_name


class CableFile(FileBase):
    folder = models.ForeignKey(
        'CableFolder',
        related_name='files',
        on_delete=models.CASCADE,
        db_column='folder_id',
    )


class CableFolder(FolderBase):
    entity = models.ForeignKey(
        'CableFile',
        related_name='folders',
        on_delete=models.CASCADE,
        db_column='entity_id',
    )


class CableSystem(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    legal_name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=200)
    operator_address_line1 = models.CharField(max_length=200)
    operator_name = models.CharField(max_length=200)
    operator_address_line2 = models.CharField(max_length=200)
    operator_po_box = models.CharField(max_length=200)
    operator_city = models.CharField(max_length=200)
    operator_zipcode = models.CharField(max_length=200)
    operator_zipcode_suffix = models.CharField(max_length=200)
    operator_state = models.CharField(max_length=2)
    operator_email = models.CharField(max_length=200, blank=True)
    operator_website = models.CharField(max_length=200, blank=True)
    operator_phone = models.CharField(max_length=200, blank=True)
    operator_fax = models.CharField(max_length=200, blank=True)

    cores_user = models.CharField(max_length=200)

    principal_headend_name = models.CharField(max_length=200, blank=True)
    principal_address_line1 = models.CharField(max_length=200, blank=True)
    principal_address_line2 = models.CharField(max_length=200, blank=True)
    principal_po_box = models.CharField(max_length=200, blank=True)
    principal_city = models.CharField(max_length=200, blank=True)
    principal_state = models.CharField(max_length=200, blank=True)
    principal_zipcode = models.CharField(max_length=200, blank=True)
    principal_zipcode_suffix = models.CharField(max_length=200, blank=True)
    principal_fax = models.CharField(max_length=200, blank=True)
    principal_phone = models.CharField(max_length=200, blank=True)
    principal_email = models.CharField(max_length=200, blank=True)

    local_file_contact_name = models.CharField(
        max_length=200, blank=True
    )
    local_file_address_line1 = models.CharField(
        max_length=200, blank=True
    )
    local_file_address_line2 = models.CharField(
        max_length=200, blank=True
    )
    local_file_po_box = models.CharField(
        max_length=200, blank=True
    )
    local_file_city = models.CharField(
        max_length=200, blank=True
    )
    local_file_state = models.CharField(
        max_length=200, blank=True
    )
    local_file_zipcode = models.CharField(
        max_length=200, blank=True
    )
    local_file_zipcode_suffix = models.CharField(
        max_length=200, blank=True
    )
    local_file_contact_fax = models.CharField(
        max_length=200, blank=True
    )
    local_file_contact_phone = models.CharField(
        max_length=200, blank=True
    )

    active_ind = models.BooleanField()
    prinicpal_address_in_local_files = models.BooleanField()
    cable_service_zip_codes = JSONField()
    cable_service_emp_units = JSONField()
    cable_communities = JSONField()

    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the cable system.
        """
        psid = self.id
        endpoint_url = f"{FCC_API_URL}/service/cable/psid/{psid}.json"

        r = requests.get(endpoint_url)

        for key, value in r.json()['results']['cableSystemInfo'].items():
            if type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False
            setattr(self, camelcase_to_underscore(key), value)

        return self.save()

    def __str__(self):
        return self.legal_name
