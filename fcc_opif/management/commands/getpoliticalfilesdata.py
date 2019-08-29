from django.core.management.base import BaseCommand, CommandError
from fcc_opif.models import Facility
import requests

class Command(BaseCommand):

    api_url = 'https://publicfiles.fcc.gov/api/'

    help = 'Get political file data for call sign and service'

    def add_arguments(self, parser):
        parser.add_argument('call_sign')
        parser.add_argument('service')

    def handle(self, *args, **options):

        facility = self.get_facility(options['call_sign'], options['service'])
        print(facility)
        self.stdout.write(self.style.SUCCESS(facility))

    def get_facility(self, call_sign, service):
        print(len(call_sign))
        print(len(service))
        facility_search_endpoint = self.api_url + 'service/facility/search/(keyword).json'
        print(facility_search_endpoint)
        r = requests.get(
            facility_search_endpoint.format(keyword=call_sign)
            )
        r.raise_for_status()
        results = r.json()['results']['globalSearchResults']
        print(results)
        key_name = service + 'ResultsCount'
        if results[key_name] == 1:
            list_name = service + 'FacilityList'
            return Facility(**results[list_name[0]])
        
    #def get_political_folder_data(self, facility):
