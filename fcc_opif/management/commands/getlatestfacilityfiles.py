'''Find a facility and get it's latest file data'''
import re
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import Facility


class Command(BaseCommand):

    help = "Find a facility and get it's latest file data."

    def add_arguments(self, parser):
        parser.add_argument('call_sign')
        parser.add_argument('service_type', choices=['am', 'fm', 'tv'])

    def handle(self, *args, **options):
        self.call_sign = options['call_sign'].upper()
        self.service_type = options['service_type'].upper()

        facilities_list = self.get_all_facilities(self.service_type)

        facility_id = self.get_facility_id(facilities_list)

        try:
            facility = Facility.objects.get(id=facility_id)
        except Facility.DoesNotExist:
            facility = Facility(
                id=facility_id,
                call_sign=self.call_sign,
                service_type=self.service_type.lower(),
            )
            msg = self.style.SUCCESS(f"{facility} was created.")
        else:
            msg = self.style.SUCCESS(f"{facility} was updated.")

        print(facility_id)

        facility.refresh_from_fcc()
        self.stdout.write(msg)
        facility.refresh_all_files()

    def get_all_facilities(self, serviceType):
        url = f"{FCC_API_URL}/service/{serviceType.lower()}/facility/getall.json"
        r = requests.get(url)
        try:
            r.raise_for_status()
        except HTTPError as e:
            raise CommandError(e)
        
        return r.json()['results']['facilityList']

    def get_facility_id(self, facilities_list):
        facility_id_lookup_dict = {
            f['callSign']: f['id'] for f in facilities_list
        }

        full_call_sign = f"{self.call_sign}-{self.service_type}"

        if self.call_sign in facility_id_lookup_dict:
            facility_id = facility_id_lookup_dict[self.call_sign]
        elif full_call_sign in facility_id_lookup_dict:
            facility_id = facility_id_lookup_dict[full_call_sign]
        else:
            raise CommandError(
                f"{self.call_sign} not found in {self.service_type} facilities."
            )

        return facility_id
