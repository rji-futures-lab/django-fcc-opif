from zappa.asynchronous import task
from django.core.management import call_command
from django.core.management.base import CommandError
from fcc_opif.models import Facility, CableSystem

logger = logging.getLogger(__name__)

@task()
def update_facility(call_sign, facility_id):
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
            'updatecablesystem', cable_system_id
        )
    except CommandError as e:
        logger.error(e)


def main():
    for facility in Facility.objects.all():
        update_facility(facility_id)
    logger.info(f'Initialized update for all facilities.')

    for cable_system in CableSystem.objects.all():
        update_cable_system(cable_system_id)
    logger.info(f'Initialized update for all cable systems.')
