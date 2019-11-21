'''Get all facilities from the FCC and save to the database'''
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import Facility
from fcc_opif.utils import json_cleaner
import logging

logger = logging.getLogger('fcc_opif.management')

class Command(BaseCommand):

    help = "Get all facilities from the FCC and save to the database."

    def handle(self, *args, **options):
        for i in SERVICE_TYPES:
            serviceType = i[0]

            logger.debug(f"Getting {serviceType} facilities...")

            raw_facilities = self.get_facilities(serviceType)

            new_facilities = self.prep_facilities(raw_facilities, serviceType)

            inserted_facilities = Facility.objects.bulk_create(new_facilities)

            logger.debug(
                f"Created {len(inserted_facilities)} new {serviceType} facilities"
            )

    def get_facilities(self, serviceType):
        url = f"{FCC_API_URL}/service/{serviceType}/facility/getall.json"
        r = requests.get(url)
        try:
            r.raise_for_status()
        except HTTPError as e:
            raise CommandError(e)

        return r.json()['results']['facilityList']

    def prep_facilities(self, facilities_list, serviceType):
        q = Facility.objects.filter(service_type=serviceType)

        existing_ids = [i['id'] for i in q.values('id')]

        new_facilities = [
            Facility(
                **json_cleaner(f), service_type=serviceType
            ).clean_api_data() for f in facilities_list
            if f['id'] not in existing_ids
        ]

        return new_facilities
