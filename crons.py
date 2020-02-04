from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Q
from zappa.asynchronous import task
from fcc_opif.models import Facility, CableSystem
import logging

logger = logging.getLogger(__name__)


@task()
def update_facility(facility_id):
    try:
        call_command(
            'updatefacility', facility_id
        )
    except CommandError as e:
        logger.error(e)


@task()
def update_cable_system(id):
    try:
        call_command(
            'getlatestcablefiles', cable_system_id
        )
    except CommandError as e:
        logger.error(e)


def handle_facilities():
    call_command('getfacilities')

    facilities = Facility.objects.order_by('last_refreshed_ts')[:30]

    for facility in facilities:
        update_facility(facility.id)
    logger.info(f'Initialized update for {len(facilities)} facilities.')


def handle_cable_systems():
    pass
    # call_command('getcablesystems')

    # for cable_system in CableSystem.objects.all():
    #     update_cable_system(cable_system.id)
    # logger.info(f'Initialized update for all cable systems.')


def main():

    handle_facilities()

    # handle_cable_systems()
