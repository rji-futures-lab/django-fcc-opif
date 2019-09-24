from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
import requests
from requests.exceptions import HTTPError
from time import sleep
from fcc_opif.constants import DOCUMENTCLOUD_PROJECT, FCC_API_URL
from fcc_opif.utils import camelcase_to_underscore, json_cleaner
from documentcloud import DocumentCloud


def get_upload_path(instance, file_name):
    return f'fcc_files/{instance.relative_path}'


class FileBase(models.Model):
    file_id = models.UUIDField(
        editable=False, max_length=200, primary_key=True
    )
    file_name = models.CharField(
        editable=False, max_length=200
    )
    file_extension = models.CharField(
        editable=False, max_length=10
    )
    file_size = models.IntegerField(
        editable=False, null=True
    )
    file_status = models.CharField(
        editable=False, max_length=200
    )
    create_ts = models.CharField(
        editable=False, max_length=200
    )
    last_update_ts = models.CharField(
        editable=False, max_length=200
    )
    file_manager_id = models.CharField(
        editable=False, max_length=200
    )
    moved_from = models.CharField(
        editable=False, max_length=200, null=True
    )
    moved_ts = models.CharField(
        editable=False, max_length=200, null=True
    )
    documentcloud_id = models.CharField(
        editable=False, max_length=200, null=True
    )
    stored_file = models.FileField(
        editable=False,
        upload_to=get_upload_path,
        blank=True,
        max_length=300,
    )

    @property
    def url(self):
        fileManagerID = self.file_manager_id
        folderID = self.folder.entity_folder_id
        return f"{FCC_API_URL}/manager/download/{folderID}/{fileManagerID}.pdf"

    @property
    def relative_path(self):
        path = f'{self.folder.entity}/{self.folder.folder_path}/{self.file_name}.{self.file_extension}'  # noqa
        return path

    def copy_to_storage(self):
        folderID = self.folder_id
        fileManagerID = self.file_manager_id
        url = f"{FCC_API_URL}/manager/download/{folderID}/{fileManagerID}.pdf"

        r = requests.get(url)
        try:
            r.raise_for_status()
        except HTTPError:
            if len(r.history) > 0:
                print('  Redirecting...')
                for rh in r.history:
                    print(f'    ...{rh.url} to...')
            print(f'   ...and finally {r.url}')
        else:
            cf = ContentFile(r.content)
            self.stored_file.save(self.relative_path, cf)

        return

    def upload_to_document_cloud(self):
        pass
        # client = DocumentCloud(
        #     settings.DOCUMENTCLOUD_USERNAME,
        #     settings.DOCUMENTCLOUD_PASSWORD,
        # )
        # doc = client.documents.upload(
        #     self.url, self.file_name,
        #     access='public', project=DOCUMENTCLOUD_PROJECT
        # )
        # sleep(2)
        # self.documentcloud_id = doc.id
        # return self.save()

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
        indexes = [
            models.Index(fields=['file_name']),
        ]


class FolderBase(models.Model):
    entity_folder_id = models.UUIDField(
        editable=False, max_length=200, primary_key=True
    )
    folder_name = models.CharField(editable=False, max_length=200)
    folder_path = models.CharField(editable=False, max_length=200)
    allow_rename_ind = models.BooleanField(editable=False)
    allow_subfolder_ind = models.BooleanField(editable=False)
    allow_upload_ind = models.BooleanField(editable=False)
    allow_delete_ind = models.BooleanField(editable=False)
    more_public_files_ind = models.BooleanField(
        editable=False, default=False
    )
    parent_folder = models.ForeignKey(
        'self',
        related_name='subfolders',
        on_delete=models.CASCADE,
        null=True,
        editable=False,
    )
    file_count = models.IntegerField(editable=False, null=True)
    create_ts = models.CharField(editable=False, max_length=200)
    last_update_ts = models.CharField(editable=False, max_length=200)

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

            fcc_updated = last_updated != file.last_update_ts
            if created or fcc_updated:
                file.copy_to_storage()
                file.upload_to_document_cloud()
                if fcc_updated:
                    file.last_update_ts = last_updated
                    file.save()

        return self.save()

    def __str__(self):
        return self.folder_path

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['folder_path']),
        ]
