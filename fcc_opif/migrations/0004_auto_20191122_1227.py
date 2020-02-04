# Generated by Django 2.2.7 on 2019-11-22 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc_opif', '0003_auto_20191120_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='last_refreshed_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='create_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cablefile',
            name='last_update_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='create_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cablefolder',
            name='last_update_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='create_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfile',
            name='last_update_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='create_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facilityfolder',
            name='last_update_ts',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]