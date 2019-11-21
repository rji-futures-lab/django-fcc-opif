'''Update a facility including all folders and files '''
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import Facility
import logging

logger = logging.getLogger('fcc_opif.management')

class Command(BaseCommand):

    help = "Update a facility including all folders and files"

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        facility_id = options['id']

        try:
            facility = Facility.objects.get(id=facility_id)
        except Facility.DoesNotExist:
            logger.debug(f"No facility with id {facility_id}.")
        else:
            facility.refresh_from_fcc()
            facility.refresh_all_files()
