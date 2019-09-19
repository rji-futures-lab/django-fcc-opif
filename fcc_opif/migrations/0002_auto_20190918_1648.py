# Generated by Django 2.2.5 on 2019-09-18 21:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import fcc_opif.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('fcc_opif', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cablefile',
            name='create_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='documentcloud_id',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='file_extension',
            field=models.CharField(editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='file_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='file_manager_id',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='file_name',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='file_size',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='file_status',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='last_update_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='moved_from',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='moved_ts',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='stored_file',
            field=models.FileField(blank=True, editable=False, max_length=300, upload_to=fcc_opif.models.base.get_upload_path),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='allow_delete_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='allow_rename_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='allow_subfolder_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='allow_upload_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='create_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='entity_folder_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='file_count',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='folder_name',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='folder_path',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='last_update_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='more_public_files_ind',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='parent_folder',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='fcc_opif.CableFolder'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='active_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='facility',
            name='auth_app_id',
            field=models.CharField(editable=False, max_length=7),
        ),
        migrations.AlterField(
            model_name='facility',
            name='band',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='call_sign',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='cc_contact',
            field=django.contrib.postgres.fields.jsonb.JSONField(editable=False),
        ),
        migrations.AlterField(
            model_name='facility',
            name='community_city',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='community_state',
            field=models.CharField(editable=False, max_length=2),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='frequency',
            field=models.DecimalField(decimal_places=1, editable=False, max_digits=4),
        ),
        migrations.AlterField(
            model_name='facility',
            name='id',
            field=models.CharField(editable=False, max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='facility',
            name='license_expiration_date',
            field=models.CharField(editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='facility',
            name='main_studio_contact',
            field=django.contrib.postgres.fields.jsonb.JSONField(editable=False),
        ),
        migrations.AlterField(
            model_name='facility',
            name='network_afil',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='nielsen_dma',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_address1',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_address2',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_city',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_name',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_phone',
            field=models.CharField(editable=False, max_length=13),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_state',
            field=models.CharField(editable=False, max_length=2),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_zip1',
            field=models.CharField(editable=False, max_length=5),
        ),
        migrations.AlterField(
            model_name='facility',
            name='party_zip2',
            field=models.CharField(blank=True, editable=False, max_length=5),
        ),
        migrations.AlterField(
            model_name='facility',
            name='post_card_id',
            field=models.CharField(editable=False, max_length=7),
        ),
        migrations.AlterField(
            model_name='facility',
            name='rf_channel',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='facility',
            name='scanned_letter_ids',
            field=models.CharField(blank=True, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='service',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='service_type',
            field=models.CharField(choices=[('am', 'AM'), ('fm', 'FM'), ('tv', 'TV')], editable=False, max_length=2),
        ),
        migrations.AlterField(
            model_name='facility',
            name='status',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facility',
            name='status_date',
            field=models.CharField(editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='facility',
            name='virtual_channel',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='create_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='documentcloud_id',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='file_extension',
            field=models.CharField(editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='file_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='file_manager_id',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='file_name',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='file_size',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='file_status',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='folder',
            field=models.ForeignKey(db_column='folder_id', editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='fcc_opif.FacilityFolder'),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='last_update_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='moved_from',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='moved_ts',
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='stored_file',
            field=models.FileField(blank=True, editable=False, max_length=300, upload_to=fcc_opif.models.base.get_upload_path),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='allow_delete_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='allow_rename_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='allow_subfolder_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='allow_upload_ind',
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='create_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='entity',
            field=models.ForeignKey(db_column='entity_id', editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='fcc_opif.Facility'),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='entity_folder_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='file_count',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='folder_name',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='folder_path',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='last_update_ts',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='more_public_files_ind',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='parent_folder',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='fcc_opif.FacilityFolder'),
        ),
    ]