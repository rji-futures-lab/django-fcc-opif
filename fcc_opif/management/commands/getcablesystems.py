'''Get all cable systems from the FCC and save to the database'''
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import CableSystem
from fcc_opif.utils import json_cleaner
import logging

logger = logging.getLogger('fcc_opif.management')

class Command(BaseCommand):

    help = "Get all cable systems from the FCC and save to the database."

    def handle(self, *args, **options):
        serviceType = 'cable'

        logger.debug(f"Getting {serviceType} systems...")

        raw_cable_systems = self.get_cable_systems(serviceType)

        new_cable_systems = self.prep_cable_systems(raw_cable_systems, serviceType)

        inserted_cable_systems = CableSystem.objects.bulk_create(new_cable_systems)

        logger.debug(
            f"Created {len(inserted_cable_systems)} new cable systems"
        )

    def get_cable_systems(self, serviceType):
        url = f"{FCC_API_URL}/service/{serviceType}/getall.json"
        r = requests.get(url)
        try:
            r.raise_for_status()
        except HTTPError as e:
            raise CommandError(e)

        return r.json()['results']['cableSystemsList']

    def prep_cable_systems(self, cable_system_list, serviceType):
        q = CableSystem.objects

        existing_ids = [i['id'] for i in q.values('id')]

        new_cable_systems = [
            CableSystem(
                **json_cleaner(cs), service_type=serviceType, id=cs['psid']
            ) for cs in cable_system_list
            if cs['psid'] not in existing_ids
        ]

        return new_cable_systems
