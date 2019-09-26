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
        
        '''
        cable_system_list = self.get_all_cable_systems()

        cable_system_id = self.get_cable_system_id(cable_system_list)
        '''

        cable_system, created = CableSystem.objects.get_or_create(id=self.id)
        if created:
            msg = self.style.SUCCESS(f"{cable_system.id} was created.")
        else:
            msg = self.style.SUCCESS(f"{cable_system.id} was updated.")

        print(self.id)

        cable_system.refresh_from_fcc()
        self.stdout.write(msg)
        cable_system.refresh_all_files()
'''
    def get_all_cable_systems(self):
        url = f"{FCC_API_URL}/service/cable/getall.json"
        r = requests.get(url)
        try:
            r.raise_for_status()
        except HTTPError as e:
            raise CommandError(e)
        
        return r.json()['results']['cableSystemsList']

    def get_cable_system_id(self, cable_system_list):
        cable_system_id_lookup_dict = {
            f['psid']: f['psid'] for f in cable_system_list
        }

        psid = self.id

        if psid in cable_system_id_lookup_dict:
            cable_system_id = cable_system_id_lookup_dict[psid]
        else:
            raise CommandError(
                f"{self.id} not found in cable systems."
            )

        return cable_system_id
'''