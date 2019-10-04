from django.apps import apps
from zappa.asynchronous import task
import logging

logger = logging.getLogger(__name__)

@task
def refresh_folder(entity_type, entity_folder_id):
    app = apps.get_app_config('fcc_opif')
    model = app.get_model(entity_type)
    folder = model.objects.get(entity_folder_id=entity_folder_id)

    logger.debug(f'Begin refresh of {folder} ({folder.entity}).')

    folder.refresh_from_fcc()

    logger.debug(f'Refresh of {folder} ({folder.entity}) ended.')

    return
