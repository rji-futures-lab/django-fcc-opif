# Generated by Django 3.0.5 on 2020-05-01 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc_opif', '0011_fileform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileform',
            name='proto_file_field',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
