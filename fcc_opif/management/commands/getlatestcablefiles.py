'''Find a facility and get it's latest file data
import re
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import CableSystem


class Command(BaseCommand):

    help = "Find a cable system and get it's latest file data."

    def add_arguments(self, parser):
        parser.add_argument('id')
        #parser.add_argument('service_type', choices=['am', 'fm', 'tv'])

    def handle(self, *args, **options):
        self.legal_name = options['call_sign'].upper()
        self.service_type = 'cable'

        cable_system_list = self.get_all_cable_systems()

        cable_system_id = self.get_cable_system_id(cable_system_list)

        try:
            cable_system = CableSystem.objects.get(id=psid)
        except CableSystem.DoesNotExist:
            cable_system = CableSystem(
                id=psid,
                #call_sign=self.call_sign,
                #service_type=self.service_type.lower(),
            )
            msg = self.style.SUCCESS(f"{cable_system} was created.")
        else:
            msg = self.style.SUCCESS(f"{cable_system} was updated.")

        print(psid)

        cable_system.refresh_from_fcc()
        self.stdout.write(msg)
        #cable_system.refresh_all_files()

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
            f['psid'] for f in cable_system_list
        }

        #full_call_sign = f"{self.legal_name}-{self.service_type}"

        if self.id in facility_id_lookup_dict:
            cable_system_id = cable_system_id_lookup_dict[self.id]
        elif full_call_sign in facility_id_lookup_dict:
            facility_id = facility_id_lookup_dict[full_call_sign]
        else:
            raise CommandError(
                f"{self.id} not found in cable facilities."
            )

        return cable_system_id
'''