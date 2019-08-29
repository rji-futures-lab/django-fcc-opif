from django.db import models
from django.contrib.postgres.fields import JSONField
from fcc_opif.constants import API_URL
from fcc_opif.utils import camelcase_to_underscore

class Facility(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    
    call_sign = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    rf_channel = models.IntegerField()
    virtual_channel = models.IntegerField()
    license_expiration_date = models.CharField(max_length=10)
    status_date = models.CharField(max_length=10)
    status = models.CharField(max_length=200)
    community_city = models.CharField(max_length=200)
    community_state = models.CharField(max_length=2) #all states abbreviated?
    facility_type = models.CharField(max_length=200)
    frequency = models.DecimalField(max_digits=4, decimal_places=1) #??
    active_ind = models.BooleanField()
    scanned_letter_ids = models.CharField(max_length=200, blank=True)
    party_name = models.CharField(max_length=200)
    party_address1 = models.CharField(max_length=200)
    party_address2 = models.CharField(max_length=200)
    party_city = models.CharField(max_length=200)
    party_zip1 = models.CharField(max_length=5)
    party_zip2 = models.CharField(max_length=5, blank=True)
    party_state = models.CharField(max_length=2)
    party_phone = models.CharField(max_length=13) #do we want specific format for phone numbers? (xxx)xxx-xxxx?
    nielsen_dma = models.CharField(max_length=200)
    network_afil = models.CharField(max_length=200)
    band = models.CharField(max_length=200)
    auth_app_id = models.CharField(max_length=7)
    post_card_id = models.CharField(max_length=7)

    main_studio_contact = JSONField()
    cc_contact = JSONField()

    def update_political_folders(self):
        folder_path_endpoint = API_URL + 'manager/folder/path.json'
        payload = {
            'folderPath': 'Political Files',
            'entityId' : self.id,
            'sourceService' : self.service
        }
        r = requests.get(folder_path_endpoint, params=payload)
        results = r.json()['folder'][0]
        self.folder_set.create(**results)
        folder_endpoint = API_URL + 'manager/folder/id/{folderID}.json'
        payload = {'entityId': self.id}
        r = requests.get(
            folder_endpoint.format(folderId=)
            )

    def __str__(self):
        return self.call_sign

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = "Facilities"

    
class Folder(models.Model):
    entity_folder_id = models.UUIDField(max_length=200, primary_key=True)
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=200)
    folder_path = models.CharField(max_length=200)
    allow_rename_ind = models.BooleanField()
    allow_subfolder_ind = models.BooleanField()
    allow_upload_ind = models.BooleanField()
    allow_delete_ind = models.BooleanField()
    parent_folder_id = models.CharField(max_length=200) #??
    file_count = models.IntegerField()
    create_ts = models.CharField(max_length=200)
    last_update_ts = models.CharField(max_length=200)

    def __str__(self):
        return self.folder_path
    
class File(models.Model):
    file_id = models.UUIDField(max_length=200, primary_key=True)

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, default = "")
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    file_extension = models.CharField(max_length=3)
    file_size = models.IntegerField()
    file_status = models.CharField(max_length=200)
    create_ts = models.CharField(max_length=200)
    last_update_ts = models.CharField(max_length=200)
    file_manager_id = models.CharField(max_length=200)

    def __str__(self):
        return self.file_name


