from django.db import models
from django.contrib.postgres.fields import JSONField
import requests
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.utils import camelcase_to_underscore, json_cleaner


class Facility(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    
    call_sign = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    service_type = models.CharField(max_length=2, choices=SERVICE_TYPES)
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


    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the facility.
        """
        serviceType = self.service_type
        entityID = self.id
        endpoint_url = f"{FCC_API_URL}/service/{serviceType}/facility/id/{entityID}.json"

        r = requests.get(endpoint_url)
        #json_cleaner(r.json['results']['facility'])
        
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
        endpoint_url = f"{FCC_API_URL}/manager/folder/parentFolders.json?entityId={entityID}&sourceService={serviceType}"

        r = requests.get(endpoint_url)

        folder_list = r.json()['folders']
        for folder_data in folder_list:
            clean_data = json_cleaner(folder_data)
            clean_data['entity_id'] = self.id
            folder, created = self.folders.update_or_create(defaults = clean_data, entity_folder_id = clean_data["entity_folder_id"])
            # import ipdb; ipdb.set_trace()
            folder.refresh_from_fcc()

        return self.save()

        # use this endpoint:
        # 'https://publicfiles.fcc.gov/api/manager/folder/parentFolders.json?entityId=65583&sourceService=tv'

    # def update_political_folders(self): 
    #     folder_path_endpoint = API_URL + 'manager/folder/path.json'
    #     payload = {
    #         'folderPath': 'Political Files',
    #         'entityId' : self.id,
    #         'sourceService' : self.service
    #     }
    #     r = requests.get(folder_path_endpoint, params=payload)
    #     results = r.json()['folder'][0]
    #     self.folder_set.create(**results)
    #     folder_endpoint = API_URL + 'manager/folder/id/{folderID}.json'
    #     payload = {'entityId': self.id}
    #     r = requests.get(
    #         folder_endpoint.format(folderId=)
    #         )

    def __str__(self):
        return self.call_sign

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = "Facilities"

    
class Folder(models.Model):
    entity_folder_id = models.UUIDField(max_length=200, primary_key=True)
    
    entity = models.ForeignKey(Facility, related_name='folders', on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=200)
    folder_path = models.CharField(max_length=200)
    allow_rename_ind = models.BooleanField()
    allow_subfolder_ind = models.BooleanField()
    allow_upload_ind = models.BooleanField()
    allow_delete_ind = models.BooleanField()
    more_public_files_ind = models.BooleanField(default = False)
    parent_folder = models.ForeignKey('self', related_name='subfolders', on_delete=models.CASCADE, null=True)
    file_count = models.IntegerField(null=True)
    create_ts = models.CharField(max_length=200)
    last_update_ts = models.CharField(max_length=200)


    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the folder and update our records.
        """
        
        entity_folder_id = self.entity_folder_id
        endpoint_url = f"{FCC_API_URL}/manager/folder/id/{entity_folder_id}.json"
        payload = {'entityId': self.entity.id}
        r = requests.get(endpoint_url, params=payload)

        for key, value in r.json()['folder'].items():
            if type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False
            if key == 'subfolders' or key == 'files':
                pass
            else:
                setattr(self, camelcase_to_underscore(key), value)
        
        for subfolder in r.json()['folder']['subfolders']:
            clean_subfolder_data = json_cleaner(subfolder)
            subfolder, created = self.subfolders.update_or_create(defaults = clean_subfolder_data, entity_folder_id = clean_subfolder_data["entity_folder_id"])
            subfolder.refresh_from_fcc()
        for file in r.json()['folder']['files']:
            clean_file_data = json_cleaner(file)
            file, created = self.files.update_or_create(defaults = clean_file_data, file_id = clean_file_data["file_id"])
                
        return self.save()


    # def update_files(self):

    #     entity_folder_id = self.entity_folder_id
    #     entityID = self.entity.id
    #     endpoint_url = f"{FCC_API_URL}/manager/folder/id/{entity_folder_id}.json"
    #     payload = {'entityId': self.entity.id}
    #     r = requests.get(endpoint_url, params=payload)
        
    #     file_list = r.json()['folder']['files']
    #     for file in file_list:
    #         for key, value in file.items():
    #             if type(value) == str:
    #                 if value.upper() == 'Y':
    #                     value = True
    #                 elif value.upper() == 'N':
    #                     value = False
    #             setattr(file, camelcase_to_underscore(key), value)           

    # def update_subfolders(self):
        
    #     for subfolder in self.subfolders:
    #         subfolder.refresh_from_fcc()


    def __str__(self):
        return self.folder_path
    
class File(models.Model):
    file_id = models.UUIDField(max_length=200, primary_key=True)

    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    file_extension = models.CharField(max_length=3)
    file_size = models.IntegerField(null = True)
    file_status = models.CharField(max_length=200)
    create_ts = models.CharField(max_length=200)
    last_update_ts = models.CharField(max_length=200)
    file_manager_id = models.CharField(max_length=200)
    moved_from = models.CharField(max_length=200, null=True)
    moved_ts = models.CharField(max_length=200, null=True)

    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the file and update our records.
        """
        
        fileID = self.file_id
        endpoint_url = f"{FCC_API_URL}/file/id/{fileID}.json"

        r = requests.get(endpoint_url)
        
        for key, value in r.json()['results']['file'].items():
            if type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False

            setattr(self, camelcase_to_underscore(key), value)
        

        return self.save()

        # use this endpoint:
        # '/file/id/{fileId}.{format}'

    def __str__(self):
        return self.file_name
