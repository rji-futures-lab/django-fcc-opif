from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Q
from django.utils import timezone
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

    yesterday = timezone.now() - timezone.timedelta(days=1)

    facilities = Facility.objects.filter(
        Q(last_refreshed_ts__isnull=True) | Q(last_refreshed_ts__gt=yesterday)
    )[:100]

    for facility in facilities:
        update_facility(facility.id)
    logger.info(f'Initialized update for {len(facilities)} facilities.')


def handle_cable_systems():
    # call_command('getcablesystems')

    # for cable_system in CableSystem.objects.all():
    #     update_cable_system(cable_system.id)
    # logger.info(f'Initialized update for all cable systems.')


def main():

    handle_facilities()

    # handle_cable_systems()
