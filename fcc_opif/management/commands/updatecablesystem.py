'''Find a cable system and get its latest file data'''
from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import HTTPError
from fcc_opif.constants import FCC_API_URL, SERVICE_TYPES
from fcc_opif.models import CableSystem
import logging

logger = logging.getLogger('fcc_opif.management')

class Command(BaseCommand):

    help = "Find a cable system and get its latest file data."

    def add_arguments(self, parser):
        parser.add_argument('id', type=str)

    def handle(self, *args, **options):
        cable_system_id = options['id']

        try:
            cable_system = CableSystem.objects.get(id=cable_system_id)
        except CableSystem.DoesNotExist:
            logger.debug(f"No cable system with id {cable_system_id}.")
        else:
            cable_system.refresh_from_fcc()
            cable_system.refresh_all_files()
