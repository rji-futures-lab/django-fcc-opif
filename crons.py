from zappa.asynchronous import task
from django.core.management import call_command
from django.core.management.base import CommandError

facilities = (
    # tv
    ('komu', 'tv'),
    ('kmiz', 'tv'),
    # ('kqfx', 'tv'),
    ('krcg', 'tv'),
    ('kmos', 'tv'),
    # am
    ('kfru', 'am'),
    ('ktgr', 'am'),
    ('kfal', 'am'),
    ('kwrt', 'am'),
    ('krll', 'am'),
    ('klik', 'am'),
    ('kwos', 'am'),
    ('kxeo', 'am'),
    ('kwix', 'am'),
    ('kmmo', 'am'),
    ('ksis', 'am'),
    ('kdro', 'am'),
    ('klti', 'am'),
    ('krms', 'am'),
    ('kwre', 'am'),
    # fm
    ('kcou', 'fm'),
    ('kjab', 'fm'),
    ('ksdq', 'fm'),
    ('kjlu', 'fm'),
    ('kopn', 'fm'),
    ('kmcv', 'fm'),
    ('kbkc', 'fm'),
    ('knlg', 'fm'),
    # ('kwwc', 'fm'),
    ('kaud', 'fm'),
    ('kbia', 'fm'),
    ('kmfc', 'fm'),
    ('ksdl', 'fm'),
    ('kwjk', 'fm'),
    ('kssz', 'fm'),
    ('kati', 'fm'),
    # ('ksdc', 'fm'),
    # ('kwwu', 'fm'),
    ('ktks', 'fm'),
    ('kwwr', 'fm'),
    ('kcmq', 'fm'),
    ('kpow', 'fm'),
    ('kclr', 'fm'),
    ('kbbm', 'fm'),
    ('ktgr', 'fm'),
    ('kpla', 'fm'),
    ('kbxr', 'fm'),
    ('kzjf', 'fm'),
    ('kres', 'fm'),
    ('kzzt', 'fm'),
    ('koql', 'fm'),
    ('ktxy', 'fm'),
    ('krfl', 'fm'),
)

cable_systems = (
    '007195',
)


@task()
def update_facility(call_sign, service_type):
    try:
        call_command(
            'getlatestfacilityfiles', call_sign, service_type
        )
    except CommandError as e:
        print(e)

@task()
def update_cable_system(id):
    try:
        call_command(
            'getlatestcablefiles', id
        )
    except CommandError as e:
        print(e)


def main():
    for facility in facilities:
        update_facility(*facility)
    num_facilities = len(facilities)
    print(f'Initialized update for all {num_facilities} facilities.')

    for cable_system in cable_systems:
        update_facility(cable_system)
    num_cable_systems = len(cable_systems)
    print(f'Initialized update for all {num_cable_systems} facilities.')
