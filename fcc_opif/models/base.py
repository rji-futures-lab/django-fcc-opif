from django.db import models
import requests
from fcc_opif.constants import DOCUMENTCLOUD_PROJECT, FCC_API_URL
from django.conf import settings
from fcc_opif.utils import camelcase_to_underscore, json_cleaner
from documentcloud import DocumentCloud


class FileBase(models.Model):
    file_id = models.UUIDField(max_length=200, primary_key=True)
    file_name = models.CharField(max_length=200)
    file_extension = models.CharField(max_length=3)
    file_size = models.IntegerField(null=True)
    file_status = models.CharField(max_length=200)
    create_ts = models.CharField(max_length=200)
    last_update_ts = models.CharField(max_length=200)
    file_manager_id = models.CharField(max_length=200)
    moved_from = models.CharField(max_length=200, null=True)
    moved_ts = models.CharField(max_length=200, null=True)
    documentcloud_id = models.CharField(max_length=200, null=True)

    @property
    def url(self):
        fileManagerID = self.file_manager_id
        folderID = self.folder.entity_folder_id
        return f"{FCC_API_URL}/manager/download/{folderID}/{fileManagerID}.pdf"

    def upload_to_cloud(self):
        client = DocumentCloud(
            settings.DOCUMENTCLOUD_USERNAME,
            settings.DOCUMENTCLOUD_PASSWORD,
        )
        doc = client.documents.upload(
            self.url, self.file_name,
            access='public', project=DOCUMENTCLOUD_PROJECT
        )
        self.documentcloud_id = doc.id
        return self.save()

    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the file and update our records.
        """
        fileID = self.file_id
        endpoint_url = f"{FCC_API_URL}/file/id/{fileID}.json"

        r = requests.get(endpoint_url)

        r.raise_for_status()

        for key, value in r.json()['results']['file'].items():
            if type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False

            setattr(self, camelcase_to_underscore(key), value)

        return self.save()

    def __str__(self):
        return self.file_name

    class Meta:
        abstract = True


class FolderBase(models.Model):
    entity_folder_id = models.UUIDField(
        max_length=200, primary_key=True
    )
    folder_name = models.CharField(max_length=200)
    folder_path = models.CharField(max_length=200)
    allow_rename_ind = models.BooleanField()
    allow_subfolder_ind = models.BooleanField()
    allow_upload_ind = models.BooleanField()
    allow_delete_ind = models.BooleanField()
    more_public_files_ind = models.BooleanField(
        default=False
    )
    parent_folder = models.ForeignKey(
        'self',
        related_name='subfolders',
        on_delete=models.CASCADE,
        null=True,
    )
    file_count = models.IntegerField(null=True)
    create_ts = models.CharField(max_length=200)
    last_update_ts = models.CharField(max_length=200)

    def refresh_from_fcc(self):
        """
        Call FCC's API to get details for the folder and update our records.
        """
        entity_folder_id = self.entity_folder_id
        endpoint_url = f"{FCC_API_URL}/manager/folder/id/{entity_folder_id}.json" # noqa
        payload = {'entityId': self.entity.id}
        r = requests.get(endpoint_url, params=payload)

        r.raise_for_status()

        for key, value in r.json()['folder'].items():
            if type(value) == str:
                if value.upper() == 'Y':
                    value = True
                elif value.upper() == 'N':
                    value = False
            elif key == 'subfolders' or key == 'files':
                pass
            else:
                setattr(self, camelcase_to_underscore(key), value)

        for subfolder in r.json()['folder']['subfolders']:
            clean_subfolder_data = json_cleaner(subfolder)
            subfolder, created = self.subfolders.update_or_create(
                defaults=clean_subfolder_data,
                entity_folder_id=clean_subfolder_data["entity_folder_id"]
            )
            subfolder.refresh_from_fcc()
        for file in r.json()['folder']['files']:
            clean_file_data = json_cleaner(file)
            last_updated = clean_file_data.pop('last_update_ts')
            file, created = self.files.update_or_create(
                defaults=clean_file_data,
                file_id=clean_file_data["file_id"]
            )
            if created:
                file.upload_to_cloud()
            elif last_updated != file.last_update_ts:
                file.upload_to_cloud()
                file.last_update_ts = last_updated
                file.save()

        return self.save()

    def __str__(self):
        return self.folder_path

    class Meta:
        abstract = True
