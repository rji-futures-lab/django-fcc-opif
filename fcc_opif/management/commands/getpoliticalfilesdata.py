import re
from django.core.management.base import BaseCommand, CommandError
from fcc_opif.models import Facility
import requests
from fcc_opif.utils import camelcase_to_underscore
from fcc_opif.constants import API_URL

class Command(BaseCommand):

    help = 'Get political file data for call sign and service'

    def add_arguments(self, parser):
        parser.add_argument('call_sign')
        parser.add_argument('service')

    def handle(self, *args, **options):    

        facility_data = self.get_facility_data(options['call_sign'], options['service'])
        reformated_data = self.reformat_facility_data(facility_data)
        print(reformated_data)
        facility = Facility(**reformated_data)
        self.stdout.write(self.style.SUCCESS(facility))

    def get_facility_data(self, call_sign, service):
        facility_search_endpoint = self.API_URL + 'service/facility/search/{keyword}.json'
        r = requests.get(
            facility_search_endpoint.format(keyword=call_sign)
            )
        r.raise_for_status()
        results = r.json()['results']['globalSearchResults']
        key_name = service + 'ResultsCount'
        if results[key_name] == 1:
            list_name = service + 'FacilityList'
            return results[list_name][0]

    def reformat_facility_data(self, facility_data):
        return {camelcase_to_underscore(k):v for (k,v) in facility_data.items()}
        
    #def get_political_folder_data(self, facility):
