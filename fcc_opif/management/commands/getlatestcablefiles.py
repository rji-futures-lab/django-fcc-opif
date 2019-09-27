'''Find a facility and get it's latest file data'''
import re
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import CableSystem


class Command(BaseCommand):

    help = "Find a cable system and get its latest file data."

    def add_arguments(self, parser):
        parser.add_argument('id')

    def handle(self, *args, **options):
        self.id = options['id'].upper()
        self.service_type = 'cable'

        cable_system, created = CableSystem.objects.get_or_create(id=self.id)
        if created:
            msg = self.style.SUCCESS(f"{cable_system.id} was created.")
        else:
            msg = self.style.SUCCESS(f"{cable_system.id} was updated.")

        cable_system.refresh_from_fcc()
        self.stdout.write(msg)
        cable_system.refresh_all_files()
